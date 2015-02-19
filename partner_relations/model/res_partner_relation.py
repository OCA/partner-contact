# -*- coding: utf-8 -*-
'''Define model res.partner.relation'''
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Therp BV (<http://therp.nl>).
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
from openerp.osv.orm import Model, except_orm
from openerp.osv import fields
from openerp.tools.translate import _


class ResPartnerRelation(Model):
    '''Model res.partner.relation is used to describe all links or relations
    between partners in the database.

    In many parts of the code we have to know whether the active partner is
    the left partner, or the right partner. If the active partner is the
    right partner we have to show the inverse name.

    Because the active partner is crucial for the working of partner
    relationships, we make sure on the res.partner model that the partner id
    is set in the context where needed.
    '''
    _name = 'res.partner.relation'
    _description = 'Partner relation'
    _order = 'active desc, date_start desc, date_end desc'

    def _on_right_partner(self, cr, uid, right_partner_id, context=None):
        '''Determine wether functions are called in a situation where the
        active partner is the right partner. Default False!
        '''
        if (context and 'active_ids' in context and
                right_partner_id in context.get('active_ids', [])):
            return True
        return False

    def _correct_vals(self, cr, uid, vals, context=None):
        '''Fill type and left and right partner id, according to wether
        we have a normal relation type or an inverse relation type'''
        vals = vals.copy()
        # If type_selection_id ends in 1, it is a reverse relation type
        if 'type_selection_id' in vals:
            prts_model = self.pool['res.partner.relation.type.selection']
            type_selection_id = vals['type_selection_id']
            (type_id, is_reverse) = (
                prts_model.get_type_from_selection_id(
                    cr, uid, type_selection_id))
            vals['type_id'] = type_id
            if context.get('active_id'):
                if is_reverse:
                    vals['right_partner_id'] = context['active_id']
                else:
                    vals['left_partner_id'] = context['active_id']
            if vals.get('partner_id_display'):
                if is_reverse:
                    vals['left_partner_id'] = vals['partner_id_display']
                else:
                    vals['right_partner_id'] = vals['partner_id_display']
        return vals

    def _get_computed_fields(
            self, cr, uid, ids, field_names, arg, context=None):
        '''Return a dictionary of dictionaries, with for every partner for
        ids, the computed values.'''
        def get_values(self, dummy_field_names, dummy_arg, context=None):
            '''Get computed values for record'''
            values = {}
            on_right_partner = self._on_right_partner(
                cr, uid, self.right_partner_id.id, context=context)
            # type_selection_id
            values['type_selection_id'] = (
                ((self.type_id.id) * 10) + (on_right_partner and 1 or 0))
            # partner_id_display
            values['partner_id_display'] = (
                self.left_partner_id.id
                if on_right_partner
                else self.right_partner_id.id
            )
            # is_relation_expired
            today = fields.date.context_today(self, cr, uid, context=context)
            values['is_relation_expired'] = (
                self.date_end and (self.date_end < today))
            # is_relation_future
            values['is_relation_future'] = self.date_start > today
            return values

        return dict([
            (i.id, get_values(i, field_names, arg, context=context))
            for i in self.browse(cr, uid, ids, context=context)
        ])

    def write(self, cr, uid, ids, vals, context=None):
        '''Override write to correct values, before being stored.'''
        vals = self._correct_vals(cr, uid, vals, context=context)
        return super(ResPartnerRelation, self).write(
            cr, uid, ids, vals, context=context)

    def create(self, cr, uid, vals, context=None):
        '''Override create to correct values, before being stored.'''
        vals = self._correct_vals(cr, uid, vals, context=context)
        return super(ResPartnerRelation, self).create(
            cr, uid, vals, context=context)

    def on_change_type_selection_id(
            self, cr, uid, dummy_ids, type_selection_id, context=None):
        '''Set domain on partner_id_display, when selection a relation type'''
        result = {
            'domain': {'partner_id_display': []},
            'value': {'type_id': False}
        }
        if not type_selection_id:
            return result
        prts_model = self.pool['res.partner.relation.type.selection']
        type_model = self.pool['res.partner.relation.type']
        (type_id, is_reverse) = (
            prts_model.get_type_from_selection_id(
                cr, uid, type_selection_id)
        )
        result['value']['type_id'] = type_id
        type_obj = type_model.browse(cr, uid, type_id, context=context)
        partner_domain = []
        check_contact_type = type_obj.contact_type_right
        check_partner_category = (
            type_obj.partner_category_right and
            type_obj.partner_category_right.id
        )
        if is_reverse:
            # partner_id_display is left partner
            check_contact_type = type_obj.contact_type_left
            check_partner_category = (
                type_obj.partner_category_left and
                type_obj.partner_category_left.id
            )
        if check_contact_type == 'c':
            partner_domain.append(('is_company', '=', True))
        if check_contact_type == 'p':
            partner_domain.append(('is_company', '=', False))
        if check_partner_category:
            partner_domain.append(
                ('category_id', 'child_of', check_partner_category))
        result['domain']['partner_id_display'] = partner_domain
        return result

    _columns = {
        'left_partner_id': fields.many2one(
            'res.partner', string='Left partner', required=True,
            auto_join=True, ondelete='cascade'),
        'right_partner_id': fields.many2one(
            'res.partner', string='Right partner', required=True,
            auto_join=True, ondelete='cascade'),
        'type_id': fields.many2one(
            'res.partner.relation.type', string='Type', required=True,
            auto_join=True),
        'date_start': fields.date('Starting date'),
        'date_end': fields.date('Ending date'),
        'type_selection_id': fields.function(
            _get_computed_fields,
            multi="computed_fields",
            fnct_inv=lambda *args: None,
            type='many2one', obj='res.partner.relation.type.selection',
            string='Type',
        ),
        'partner_id_display': fields.function(
            _get_computed_fields,
            multi="computed_fields",
            fnct_inv=lambda *args: None,
            type='many2one', obj='res.partner',
            string='Partner'
        ),
        'is_relation_expired': fields.function(
            _get_computed_fields,
            multi="computed_fields",
            type='boolean',
            method=True,
            string='Relation is expired',
        ),
        'is_relation_future': fields.function(
            _get_computed_fields,
            multi="computed_fields",
            type='boolean',
            method=True,
            string='Relation is in the future',
        ),
        'active': fields.boolean('Active'),
    }

    _defaults = {
        'active': True,
    }

    def _check_dates(self, cr, uid, ids, context=None):
        '''End date should not be before start date, if noth filled'''
        for line in self.browse(cr, uid, ids, context=context):
            if line.date_start and line.date_end:
                if line.date_start > line.date_end:
                    return False
        return True

    def _check_partner_type_left(self, cr, uid, ids, context=None):
        '''Check left partner for required company or person'''
        for this in self.browse(cr, uid, ids, context=context):
            ptype = this.type_id.contact_type_left
            company = this.left_partner_id.is_company
            if (ptype == 'c' and not company) or (ptype == 'p' and company):
                return False
        return True

    def _check_partner_type_right(self, cr, uid, ids, context=None):
        '''Check right partner for required company or person'''
        for this in self.browse(cr, uid, ids, context=context):
            ptype = this.type_id.contact_type_right
            company = this.right_partner_id.is_company
            if (ptype == 'c' and not company) or (ptype == 'p' and company):
                return False
        return True

    def _check_not_with_self(self, cr, uid, ids, context=None):
        '''Not allowed to link partner to same partner'''
        for this in self.browse(cr, uid, ids, context=context):
            if this.left_partner_id == this.right_partner_id:
                return False
        return True

    def _check_relation_uniqueness(self, cr, uid, ids, context=None):
        '''Forbid multiple active relations of the same type between the same
        partners'''
        for this in self.browse(cr, uid, ids, context=context):
            if not this.active:
                continue
            domain = [
                ('type_id', '=', this.type_id.id),
                ('active', '=', True),
                ('id', '!=', this.id),
                ('left_partner_id', '=', this.left_partner_id.id),
                ('right_partner_id', '=', this.right_partner_id.id),
                ]
            if this.date_start:
                domain += ['|', ('date_end', '=', False),
                                ('date_end', '>=', this.date_start)]
            if this.date_end:
                domain += ['|', ('date_start', '=', False),
                                ('date_start', '<=', this.date_end)]
            if self.search(cr, uid, domain, context=context):
                raise except_orm(
                    _('Overlapping relation'),
                    _('There is already a similar relation '
                      'with overlapping dates'))

        return True

    _constraints = [
        (
            _check_dates,
            'The starting date cannot be after the ending date.',
            ['date_start', 'date_end']
        ),
        (
            _check_partner_type_left,
            'The left partner is not applicable for this relation type.',
            ['left_partner_id', 'type_id']
        ),
        (
            _check_partner_type_right,
            'The right partner is not applicable for this relation type.',
            ['right_partner_id', 'type_id']
        ),
        (
            _check_not_with_self,
            'Partners cannot have a relation with themselves.',
            ['left_partner_id', 'right_partner_id']
        ),
        (
            _check_relation_uniqueness,
            "The same relation can't be created twice.",
            ['left_partner_id', 'right_partner_id', 'active']
        )
    ]

    def get_action_related_partners(self, cr, uid, ids, context=None):
        '''return a window action showing a list of partners taking part in the
        relations names by ids. Context key 'partner_relations_show_side'
        determines if we show 'left' side, 'right' side or 'all' (default)
        partners.
        If active_model is res.partner.relation.all, left=this and
        right=other'''
        if context is None:
            context = {}

        field_names = {}

        if context.get('active_model', self._name) == self._name:
            field_names = {
                'left': ['left'],
                'right': ['right'],
                'all': ['left', 'right']
            }
        elif context.get('active_model') == 'res.partner.relation.all':
            field_names = {
                'left': ['this'],
                'right': ['other'],
                'all': ['this', 'other']
            }
        else:
            assert False, 'Unknown active_model!'

        partner_ids = []
        field_names = field_names[
            context.get('partner_relations_show_side', 'all')]
        field_names = ['%s_partner_id' % n for n in field_names]

        for relation in self.pool[context.get('active_model')].read(
                cr, uid, ids, context=context, load='_classic_write'):
            for name in field_names:
                partner_ids.append(relation[name])

        return {
            'name': _('Related partners'),
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'domain': [('id', 'in', partner_ids)],
            'views': [(False, 'tree'), (False, 'form')],
            'view_type': 'form'
        }
