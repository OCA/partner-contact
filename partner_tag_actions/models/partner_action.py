# -*- coding: utf-8 -*-
# Copyright 2016 Savoir-faire Linux
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class PartnerAction(models.Model):
    _name = 'partner.action'
    _description = 'Partner Action'
    _order = "priority"

    def _get_name(self):
        for record in self:
            record.name = u"{0} [{1}] {2}".format(
                record.date,
                record.action_type.name,
                record.partner_id.name,
            )

    # Fields
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 required=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', string='User',
                              required=True, readonly=True,
                              default=lambda self: self.env.user)
    name = fields.Char(compute=_get_name)

    date = fields.Date('Date', required=True,
                       default=fields.Date.context_today)
    date_start = fields.Date('Start Date',
                             default=fields.Date.context_today)
    date_end = fields.Date('End Date')

    details = fields.Text('Details')

    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done')],
                             string='Status', required=True,
                             default='draft')

    action_type = fields.Many2one(
        'partner.action.type', string='Type', required=True,
        default=lambda self: self.env['partner.action.type'].get_default(),
    )
    is_active = fields.Boolean(help="Currently active")
    priority = fields.Integer(related="action_type.priority", store=True)

    @api.constrains('date_start', 'date_end')
    def check_dates(self):
        if self.date_start and self.date_end and \
                self.date_start > self.date_end:
            raise ValidationError(
                _('The end date cannot precede the start date!')
            )

    # Button actions
    @api.multi
    def button_confirm(self):
        self.write({'state': 'done'})
        self.apply_partner()

    @api.multi
    def button_draft(self):
        self.write({'state': 'draft'})
        self.apply_partner()

    def check_date_active(self):
        today = fields.Date.context_today(self)
        start = self.date_start or today
        end = self.date_end or today
        return start <= today <= end

    @api.depends('date_start', 'date_end', 'state')
    def check_is_active(self, single=False):
        """
        Make sure an action is in/active according to its state and
        dates, correcting its status as required.

        If `single` is True, re-apply partner rules when necessary
        """
        if self.state == 'done' and self.check_date_active():
            if not self.is_active:
                self.is_active = True
        elif self.is_active:
            self.action_outdated(single=single)

    def action_outdated(self, single=False):
        """
        Tag action is outdated, revert its changes

        if `single` is True, re-apply partner actions
        """
        if not self.is_active:
            return

        self.is_active = False
        action = self.action_type
        if action.add_tag:
            self.partner_id.category_id -= action.add_tag

        if not single:
            # We re-apply partner actions because this action may have
            # prevented another one from applying
            self.apply_partner()
        return True

    # Cron
    @api.model
    def apply_active_actions(self):
        # We may want to limit this to actions that have start/end dates
        # around today to pick up changes when appropriate
        active_actions = self.search(
            [('state', '=', 'done')],
            order="partner_id, priority DESC")

        return active_actions.apply_all()

    @api.multi
    def apply_all(self):
        """ Apply all actions in the order they are passed """
        partner_writes = {}
        partners = {}
        tag_obj = self.env["res.partner.category"]
        # Collect the result of all add/remove tags
        for action in self:
            action.check_is_active(single=True)
            if not action.is_active:
                continue

            partner = partner_writes.setdefault(action.partner_id.id,
                                                {"+": set(), "-": set()})
            partners.setdefault(action.partner_id.id, action.partner_id)
            atype = action.action_type
            if atype.add_tag:
                partner["+"].add(atype.add_tag.id)
                partner["-"].discard(atype.add_tag.id)
            if atype.remove_tag:
                partner["-"].add(atype.remove_tag.id)
                partner["+"].discard(atype.remove_tag.id)

        # Apply necessary changes to tags
        for partner_id, changes in partner_writes.iteritems():
            partner = partners[partner_id]
            for tag in tag_obj.browse(changes["-"]):
                partner.category_id -= tag
            for tag in tag_obj.browse(changes["+"]):
                partner.category_id |= tag

        return True

    @api.multi
    def apply_partner(self):
        partner = self.mapped(lambda x: x.partner_id)
        partner.apply_actions()
        return True

    # Overriden methods to make sure changes are applied
    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        res = super(PartnerAction, self).create(vals)
        res.apply_partner()
        return res

    @api.multi
    def write(self, vals):
        res = super(PartnerAction, self).write(vals)
        self.apply_partner()
        return res
