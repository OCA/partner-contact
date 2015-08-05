# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api


class PartnerAction(models.Model):
    _name = 'partner.action'
    _description = 'Partner Action'
    _order = "priority"

    # Getters/Setters
    def _get_done(self):
        for record in self:
            self.done = record.state == 'done'

    def _set_done(self):
        for record in self:
            self.state = 'done' if self.done else 'draft'

    def _get_name(self):
        for record in self:
            self.name = u"{0} [{1}] {2}".format(
                self.date,
                self.action_type.name,
                self.partner_id.name,
            )

    @api.depends('action_type.is_active', 'date_start', 'date_end', 'state')
    @api.one
    def _get_active(self):
        today = fields.Date.context_today(self)
        self.action_active = all([
            self.action_type.is_active,
            self.state == 'done',
            not self.date_start or self.date_start <= today,
            not self.date_end or self.date_end >= today,
        ])

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
    date_end = fields.Date('End Date',
                           default=fields.Date.context_today)

    details = fields.Text('Details')

    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done')],
                             string='Status', reuqired=True,
                             default='draft')

    action_type = fields.Many2one(
        'partner.action.type', string='Type', required=True,
        default=lambda self: self.env['partner.action.type'].get_default(),
    )
    priority = fields.Integer(related="action_type.priority", store=True)
    action_active = fields.Boolean(compute=_get_active, store=True)

    done = fields.Boolean(compute=_get_done, inverse=_set_done)

    # Button actions
    @api.multi
    def button_confirm(self):
        self.write({'state': 'done'})
        self.apply_partner()

    @api.multi
    def button_draft(self):
        self.write({'state': 'draft'})
        self.apply_partner()

    # Cron
    @api.model
    def apply_active_actions(self):
        active_actions = self.search(
            [('action_active', '=', True)],
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
                partner.category_id += tag

        return True

    @api.multi
    @api.depends('state')
    def apply_partner(self):
        partner = self.mapped(lambda x: x.partner_id)
        actions = self.search(
            [('action_active', '=', True),
             ('partner_id', '=', partner.id)],
            order="priority DESC")
        return actions.apply_all()

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        res = super(PartnerAction, self).create(vals)
        res.apply_partner()
        return res
