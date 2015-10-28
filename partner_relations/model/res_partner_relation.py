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

from openerp import osv, models, fields, api, exceptions, _

from . import get_partner_type


class ResPartnerRelation(models.Model):
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

    def _search_any_partner_id(self, operator, value):
        return [
            '|',
            ('left_partner_id', operator, value),
            ('right_partner_id', operator, value),
        ]

    def _get_computed_fields(
            self, cr, uid, ids, field_names, arg, context=None):
        '''Return a dictionary of dictionaries, with for every partner for
        ids, the computed values.'''
        def get_values(self, dummy_field_names, dummy_arg, context=None):
            '''Get computed values for record'''
            values = {}
            on_right_partner = self._on_right_partner(self.right_partner_id.id)
            # type_selection_id
            values['type_selection_id'] = (
                ((self.type_id.id) * 10) + (on_right_partner and 1 or 0))
            # partner_id_display
            values['partner_id_display'] = (
                self.left_partner_id.id
                if on_right_partner
                else self.right_partner_id.id
            )
            return values

        return dict([
            (i.id, get_values(i, field_names, arg, context=context))
            for i in self.browse(cr, uid, ids, context=context)
        ])

    _columns = {
        'type_selection_id': osv.fields.function(
            _get_computed_fields,
            multi="computed_fields",
            fnct_inv=lambda *args: None,
            type='many2one', obj='res.partner.relation.type.selection',
            string='Type',
        ),
        'partner_id_display': osv.fields.function(
            _get_computed_fields,
            multi="computed_fields",
            fnct_inv=lambda *args: None,
            type='many2one', obj='res.partner',
            string='Partner'
        ),
    }

    allow_self = fields.Boolean(related='type_id.allow_self')
    left_contact_type = fields.Selection(
        lambda s: s.env['res.partner.relation.type']._get_partner_types(),
        'Left Partner Type',
        compute='_get_partner_type_any',
        store=True,
    )

    right_contact_type = fields.Selection(
        lambda s: s.env['res.partner.relation.type']._get_partner_types(),
        'Right Partner Type',
        compute='_get_partner_type_any',
        store=True,
    )

    any_partner_id = fields.Many2many(
        'res.partner',
        string='Partner',
        compute='_get_partner_type_any',
        search='_search_any_partner_id'
    )

    left_partner_id = fields.Many2one(
        'res.partner',
        string='Source Partner',
        required=True,
        auto_join=True,
        ondelete='cascade',
    )

    right_partner_id = fields.Many2one(
        'res.partner',
        string='Destination Partner',
        required=True,
        auto_join=True,
        ondelete='cascade',
    )

    type_id = fields.Many2one(
        'res.partner.relation.type',
        string='Type',
        required=True,
        auto_join=True,
    )

    date_start = fields.Date('Starting date')
    date_end = fields.Date('Ending date')
    active = fields.Boolean('Active', default=True)

    @api.one
    @api.depends('left_partner_id', 'right_partner_id')
    def _get_partner_type_any(self):
        self.left_contact_type = get_partner_type(self.left_partner_id)
        self.right_contact_type = get_partner_type(self.right_partner_id)

        self.any_partner_id = self.left_partner_id + self.right_partner_id

    def _on_right_partner(self, cr, uid, right_partner_id, context=None):
        '''Determine wether functions are called in a situation where the
        active partner is the right partner. Default False!
        '''
        if (context and 'active_ids' in context and
                right_partner_id in context.get('active_ids', [])):
            return True
        return False

    def _correct_vals(self, vals):
        """Fill type and left and right partner id, according to whether
        we have a normal relation type or an inverse relation type
        """
        vals = vals.copy()
        # If type_selection_id ends in 1, it is a reverse relation type
        if 'type_selection_id' in vals:
            prts_model = self.env['res.partner.relation.type.selection']
            type_selection_id = vals['type_selection_id']
            (type_id, is_reverse) = (
                prts_model.browse(type_selection_id).
                get_type_from_selection_id()
            )
            vals['type_id'] = type_id
            if self._context.get('active_id'):
                if is_reverse:
                    vals['right_partner_id'] = self._context['active_id']
                else:
                    vals['left_partner_id'] = self._context['active_id']
            if vals.get('partner_id_display'):
                if is_reverse:
                    vals['left_partner_id'] = vals['partner_id_display']
                else:
                    vals['right_partner_id'] = vals['partner_id_display']
            if vals.get('other_partner_id'):
                if is_reverse:
                    vals['left_partner_id'] = vals['other_partner_id']
                else:
                    vals['right_partner_id'] = vals['other_partner_id']
                del vals['other_partner_id']
            if vals.get('contact_type'):
                del vals['contact_type']
        return vals

    @api.multi
    def write(self, vals):
        """Override write to correct values, before being stored."""
        vals = self._correct_vals(vals)
        return super(ResPartnerRelation, self).write(vals)

    @api.model
    def create(self, vals):
        """Override create to correct values, before being stored."""
        vals = self._correct_vals(vals)
        return super(ResPartnerRelation, self).create(vals)

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

    @api.one
    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        """End date should not be before start date, if not filled

        :raises exceptions.Warning: When constraint is violated
        """
        if (self.date_start and self.date_end and
                self.date_start > self.date_end):
            raise exceptions.Warning(
                _('The starting date cannot be after the ending date.')
            )

    @api.one
    @api.constrains('left_partner_id', 'type_id')
    def _check_partner_type_left(self):
        """Check left partner for required company or person

        :raises exceptions.Warning: When constraint is violated
        """
        self._check_partner_type("left")

    @api.one
    @api.constrains('right_partner_id', 'type_id')
    def _check_partner_type_right(self):
        """Check right partner for required company or person

        :raises exceptions.Warning: When constraint is violated
        """
        self._check_partner_type("right")

    @api.one
    def _check_partner_type(self, side):
        """Check partner to left or right for required company or person

        :param str side: left or right
        :raises exceptions.Warning: When constraint is violated
        """
        assert side in ['left', 'right']
        ptype = getattr(self.type_id, "contact_type_%s" % side)
        company = getattr(self, '%s_partner_id' % side).is_company
        if (ptype == 'c' and not company) or (ptype == 'p' and company):
            raise exceptions.Warning(
                _('The %s partner is not applicable for this relation type.') %
                side
            )

    @api.one
    @api.constrains('left_partner_id', 'right_partner_id')
    def _check_not_with_self(self):
        """Not allowed to link partner to same partner

        :raises exceptions.Warning: When constraint is violated
        """
        if self.left_partner_id == self.right_partner_id:
            if not self.allow_self:
                raise exceptions.Warning(
                    _('Partners cannot have a relation with themselves.')
                )

    @api.one
    @api.constrains('left_partner_id', 'right_partner_id', 'active')
    def _check_relation_uniqueness(self):
        """Forbid multiple active relations of the same type between the same
        partners

        :raises exceptions.Warning: When constraint is violated
        """
        if not self.active:
            return
        domain = [
            ('type_id', '=', self.type_id.id),
            ('active', '=', True),
            ('id', '!=', self.id),
            ('left_partner_id', '=', self.left_partner_id.id),
            ('right_partner_id', '=', self.right_partner_id.id),
        ]
        if self.date_start:
            domain += ['|', ('date_end', '=', False),
                            ('date_end', '>=', self.date_start)]
        if self.date_end:
            domain += ['|', ('date_start', '=', False),
                            ('date_start', '<=', self.date_end)]
        if self.search(domain):
            raise exceptions.Warning(
                _('There is already a similar relation with overlapping dates')
            )

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
