# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, _, api
from openerp.osv import expression


class ResPartner(models.Model):
    _inherit = 'res.partner'

    contact_type = fields.Selection(
        [('standalone', _('Standalone Contact')),
         ('attached', _('Attached to existing Contact')),
         ],
        compute='_get_contact_type',
        required=True, select=1, store=True,
        default='standalone')
    contact_id = fields.Many2one('res.partner', string='Main Contact',
                                 domain=[('is_company', '=', False),
                                         ('contact_type', '=', 'standalone'),
                                         ],
                                 )
    other_contact_ids = fields.One2many('res.partner', 'contact_id',
                                        string='Others Positions')

    @api.one
    @api.depends('contact_id')
    def _get_contact_type(self):
        self.contact_type = self.contact_id and 'attached' or 'standalone'

    def _basecontact_check_context(self, mode):
        """ Remove 'search_show_all_positions' for non-search mode.
        Keeping it in context can result in unexpected behaviour (ex: reading
        one2many might return wrong result - i.e with "attached contact"
        removed even if it's directly linked to a company).
        Actually, is easier to override a dictionary value to indicate it
        should be ignored...
        """
        if (mode != 'search' and
                'search_show_all_positions' in self.env.context):
            result = self.with_context(
                search_show_all_positions={'is_set': False})
        else:
            result = self
        return result

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        """ Display only standalone contact matching ``args`` or having
        attached contact matching ``args`` """
        ctx = self.env.context
        if (ctx.get('search_show_all_positions', {}).get('is_set') and
                not ctx['search_show_all_positions']['set_value']):
            args = expression.normalize_domain(args)
            attached_contact_args = expression.AND(
                (args, [('contact_type', '=', 'attached')])
            )
            attached_contacts = super(ResPartner, self).search(
                attached_contact_args)
            args = expression.OR((
                expression.AND(([('contact_type', '=', 'standalone')], args)),
                [('other_contact_ids', 'in', attached_contacts.ids)],
            ))
        return super(ResPartner, self).search(args, offset=offset,
                                              limit=limit, order=order,
                                              count=count)

    @api.model
    def create(self, vals):
        """ When creating, use a modified self to alter the context (see
        comment in _basecontact_check_context).  Also, we need to ensure
        that the name on an attached contact is the same as the name on the
        contact it is attached to."""
        modified_self = self._basecontact_check_context('create')
        if not vals.get('name') and vals.get('contact_id'):
            vals['name'] = modified_self.browse(vals['contact_id']).name
        return super(ResPartner, modified_self).create(vals)

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        modified_self = self._basecontact_check_context('read')
        return super(ResPartner, modified_self).read(fields=fields, load=load)

    @api.multi
    def write(self, vals):
        modified_self = self._basecontact_check_context('write')
        return super(ResPartner, modified_self).write(vals)

    @api.multi
    def unlink(self):
        modified_self = self._basecontact_check_context('unlink')
        return super(ResPartner, modified_self).unlink()

    @api.multi
    def _commercial_partner_compute(self, name, args):
        """ Returns the partner that is considered the commercial
        entity of this partner. The commercial entity holds the master data
        for all commercial fields (see :py:meth:`~_commercial_fields`) """
        result = super(ResPartner, self)._commercial_partner_compute(name,
                                                                     args)
        for partner in self:
            if partner.contact_type == 'attached' and not partner.parent_id:
                result[partner.id] = partner.contact_id.id
        return result

    def _contact_fields(self):
        """ Returns the list of contact fields that are synced from the parent
        when a partner is attached to him. """
        return ['name', 'title']

    def _contact_sync_from_parent(self):
        """ Handle sync of contact fields when a new parent contact entity
        is set, as if they were related fields
        """
        self.ensure_one()
        if self.contact_id:
            contact_fields = self._contact_fields()
            sync_vals = self._update_fields_values(self.contact_id,
                                                   contact_fields)
            self.write(sync_vals)

    def update_contact(self, vals):
        if self.env.context.get('__update_contact_lock'):
            return
        contact_fields = self._contact_fields()
        contact_vals = dict(
            (field, vals[field]) for field in contact_fields if field in vals
        )
        if contact_vals:
            self.with_context(__update_contact_lock=True).write(contact_vals)

    @api.model
    def _fields_sync(self, partner, update_values):
        """Sync commercial fields and address fields from company and to
        children, contact fields from contact and to attached contact
        after create/update, just as if those were all modeled as
        fields.related to the parent
        """
        super(ResPartner, self)._fields_sync(partner, update_values)
        contact_fields = self._contact_fields()
        # 1. From UPSTREAM: sync from parent contact
        if update_values.get('contact_id'):
            partner._contact_sync_from_parent()
        # 2. To DOWNSTREAM: sync contact fields to parent or related
        elif any(field in contact_fields for field in update_values):
            update_ids = [
                c.id for c in partner.other_contact_ids if not c.is_company
            ]
            if partner.contact_id:
                update_ids.append(partner.contact_id.id)
            self.browse(update_ids).update_contact(update_values)

    @api.onchange('contact_id')
    def _onchange_contact_id(self):
        if self.contact_id:
            self.name = self.contact_id.name

    @api.onchange('contact_type')
    def _onchange_contact_type(self):
        if self.contact_type == 'standalone':
            self.contact_id = False
