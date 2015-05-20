# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-TODAY OpenERP SA (<http://www.openerp.com>).
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

from openerp.osv import fields, orm, expression
from openerp.tools.translate import _


class res_partner(orm.Model):
    _inherit = 'res.partner'

    def _type_selection(self, cr, uid, context=None):
        return [
            ('standalone', _('Standalone Contact')),
            ('attached', _('Attached to existing Contact')),
        ]

    def _get_contact_type(self, cr, uid, ids, field_name, args, context=None):
        result = dict.fromkeys(ids, 'standalone')
        for partner in self.browse(cr, uid, ids, context=context):
            if partner.contact_id:
                result[partner.id] = 'attached'
        return result

    _columns = {
        'contact_type': fields.function(
            _get_contact_type,
            type='selection',
            selection=lambda self, *a, **kw: self._type_selection(*a, **kw),
            string='Contact Type',
            required=True,
            select=1,
            store=True,
        ),
        'contact_id': fields.many2one(
            'res.partner',
            'Main Contact',
            domain=[
                ('is_company', '=', False),
                ('contact_type', '=', 'standalone'),
            ],
        ),
        'other_contact_ids': fields.one2many(
            'res.partner',
            'contact_id',
            'Others Positions',
        ),
    }

    _defaults = {
        'contact_type': 'standalone',
    }

    def _basecontact_check_context(self, cr, user, mode, context=None):
        """ Remove 'search_show_all_positions' for non-search mode.
        Keeping it in context can result in unexpected behaviour (ex: reading
        one2many might return wrong result - i.e with "attached contact"
        removed even if it's directly linked to a company).
        """
        context = dict(context or {})
        if mode != 'search':
            context.pop('search_show_all_positions', None)
        return context

    def search(
            self, cr, user, args, offset=0, limit=None, order=None,
            context=None, count=False):
        """ Display only standalone contact matching ``args`` or having
        attached contact matching ``args`` """
        if context is None:
            context = {}
        if context.get('search_show_all_positions') is False:
            args = expression.normalize_domain(args)
            attached_contact_args = expression.AND(
                (args, [('contact_type', '=', 'attached')])
            )
            attached_contact_ids = super(res_partner, self).search(
                cr, user, attached_contact_args, context=context
            )
            args = expression.OR((
                expression.AND(([('contact_type', '=', 'standalone')], args)),
                [('other_contact_ids', 'in', attached_contact_ids)],
            ))
        return super(res_partner, self).search(
            cr, user, args, offset=offset, limit=limit, order=order,
            context=context, count=count
        )

    def create(self, cr, user, vals, context=None):
        context = self._basecontact_check_context(cr, user, 'create', context)
        if not vals.get('name') and vals.get('contact_id'):
            vals['name'] = self.browse(
                cr, user, vals['contact_id'], context=context).name
        return super(res_partner, self).create(cr, user, vals, context=context)

    def read(
            self, cr, user, ids, fields=None, context=None,
            load='_classic_read'):
        context = self._basecontact_check_context(cr, user, 'read', context)
        return super(res_partner, self).read(
            cr, user, ids, fields=fields, context=context, load=load)

    def write(self, cr, user, ids, vals, context=None):
        context = self._basecontact_check_context(cr, user, 'write', context)
        return super(
            res_partner, self).write(cr, user, ids, vals, context=context)

    def unlink(self, cr, user, ids, context=None):
        context = self._basecontact_check_context(cr, user, 'unlink', context)
        return super(res_partner, self).unlink(cr, user, ids, context=context)

    def _commercial_partner_compute(
            self, cr, uid, ids, name, args, context=None):
        """ Returns the partner that is considered the commercial
        entity of this partner. The commercial entity holds the master data
        for all commercial fields (see :py:meth:`~_commercial_fields`) """
        result = super(res_partner, self)._commercial_partner_compute(
            cr, uid, ids, name, args, context=context)
        for partner in self.browse(cr, uid, ids, context=context):
            if partner.contact_type == 'attached' and not partner.parent_id:
                result[partner.id] = partner.contact_id.id
        return result

    def _contact_fields(self, cr, uid, context=None):
        """ Returns the list of contact fields that are synced from the parent
        when a partner is attached to him. """
        return ['name', 'title']

    def _contact_sync_from_parent(self, cr, uid, partner, context=None):
        """ Handle sync of contact fields when a new parent contact entity
        is set, as if they were related fields
        """
        if partner.contact_id:
            contact_fields = self._contact_fields(cr, uid, context=context)
            sync_vals = self._update_fields_values(
                cr, uid, partner.contact_id, contact_fields, context=context
            )
            partner.write(sync_vals)

    def update_contact(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        if context.get('__update_contact_lock'):
            return
        contact_fields = self._contact_fields(cr, uid, context=context)
        contact_vals = dict(
            (field, vals[field]) for field in contact_fields if field in vals
        )
        if contact_vals:
            ctx = dict(context, __update_contact_lock=True)
            self.write(cr, uid, ids, contact_vals, context=ctx)

    def _fields_sync(self, cr, uid, partner, update_values, context=None):
        """Sync commercial fields and address fields from company and to
        children, contact fields from contact and to attached contact
        after create/update, just as if those were all modeled as
        fields.related to the parent
        """
        super(res_partner, self)._fields_sync(
            cr, uid, partner, update_values, context=context
        )
        contact_fields = self._contact_fields(cr, uid, context=context)
        # 1. From UPSTREAM: sync from parent contact
        if update_values.get('contact_id'):
            self._contact_sync_from_parent(cr, uid, partner, context=context)
        # 2. To DOWNSTREAM: sync contact fields to parent or related
        elif any(field in contact_fields for field in update_values):
            update_ids = [
                c.id for c in partner.other_contact_ids if not c.is_company
            ]
            if partner.contact_id:
                update_ids.append(partner.contact_id.id)
            self.update_contact(
                cr, uid, update_ids, update_values, context=context
            )

    def onchange_contact_id(self, cr, uid, ids, contact_id, context=None):
        values = {}
        if contact_id:
            values['name'] = self.browse(
                cr, uid, contact_id, context=context).name
        return {'value': values}

    def onchange_contact_type(self, cr, uid, ids, contact_type, context=None):
        values = {}
        if contact_type == 'standalone':
            values['contact_id'] = False
        return {'value': values}


class ir_actions_window(orm.Model):
    _inherit = 'ir.actions.act_window'

    def read(
            self, cr, user, ids, fields=None, context=None,
            load='_classic_read'):
        action_ids = ids
        if isinstance(ids, (int, long)):
            action_ids = [ids]
        actions = super(ir_actions_window, self).read(
            cr, user, action_ids, fields=fields, context=context, load=load
        )
        for action in actions:
            if action.get('res_model', '') == 'res.partner':
                # By default, only show standalone contact
                action_context = action.get('context', '{}') or '{}'
                if 'search_show_all_positions' not in action_context:
                    action['context'] = action_context.replace(
                        '{', "{'search_show_all_positions': False,", 1
                    )
        if isinstance(ids, (int, long)):
            if actions:
                return actions[0]
            return False
        return actions
