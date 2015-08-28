# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Therp BV (<http://therp.nl>).
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
from openerp.tools import drop_view_if_exists
from .res_partner_relation_type_selection import \
    ResPartnerRelationTypeSelection
from . import get_partner_type, PADDING


class ResPartnerRelationAll(models.AbstractModel):
    _auto = False
    _log_access = False
    _name = 'res.partner.relation.all'
    _overlays = 'res.partner.relation'
    _description = 'All (non-inverse + inverse) relations between partners'

    _additional_view_fields = []
    '''append to this list if you added fields to res_partner_relation that
    you need in this model and related fields are not adequate (ie for sorting)
    You must use the same name as in res_partner_relation.
    Don't overwrite this list in your declaration but append in _auto_init:

    def _auto_init(self, cr, context=None):
        self._additional_view_fields.append('my_field')
        return super(ResPartnerRelationAll, self)._auto_init(
            cr, context=context)

    my_field = fields...
    '''

    this_partner_id = fields.Many2one(
        'res.partner',
        string='Current Partner',
        required=True,
    )

    other_partner_id = fields.Many2one(
        'res.partner',
        string='Other Partner',
        required=True,
    )

    type_id = fields.Many2one(
        'res.partner.relation.type',
        string='Relation Type',
        required=True,
    )

    type_selection_id = fields.Many2one(
        'res.partner.relation.type.selection',
        string='Relation Type',
        required=True,
    )

    relation_id = fields.Many2one(
        'res.partner.relation',
        'Relation',
        readonly=True,
    )

    record_type = fields.Selection(
        ResPartnerRelationTypeSelection._RECORD_TYPES,
        'Record Type',
        readonly=True,
    )

    contact_type = fields.Selection(
        lambda s: s.env['res.partner.relation.type']._get_partner_types(),
        'Partner Type',
        default=lambda self: self._get_default_contact_type()
    )

    date_start = fields.Date('Starting date')
    date_end = fields.Date('Ending date')
    active = fields.Boolean('Active', default=True)

    def _auto_init(self, cr, context=None):
        drop_view_if_exists(cr, self._table)
        additional_view_fields = ','.join(self._additional_view_fields)
        additional_view_fields = (',' + additional_view_fields)\
            if additional_view_fields else ''
        cr.execute(
            '''create or replace view %(table)s as
            select
                id * %(padding)d as id,
                id as relation_id,
                type_id,
                cast('a' as char(1)) as record_type,
                left_contact_type as contact_type,
                left_partner_id as this_partner_id,
                right_partner_id as other_partner_id,
                date_start,
                date_end,
                active,
                type_id * %(padding)d as type_selection_id
                %(additional_view_fields)s
            from %(underlying_table)s
            union select
                id * %(padding)d + 1,
                id,
                type_id,
                cast('b' as char(1)),
                right_contact_type,
                right_partner_id,
                left_partner_id,
                date_start,
                date_end,
                active,
                type_id * %(padding)d + 1
                %(additional_view_fields)s
            from %(underlying_table)s''' % {
                'table': self._table,
                'padding': PADDING,
                'additional_view_fields': additional_view_fields,
                'underlying_table': 'res_partner_relation',
            }
        )

        return super(ResPartnerRelationAll, self)._auto_init(
            cr, context=context)

    def _get_underlying_object(self):
        """Get the record on which this record is overlaid"""
        return self.env[self._overlays].browse(self.id / PADDING)

    def _get_default_contact_type(self):
        partner_id = self._context.get('default_this_partner_id')
        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            return get_partner_type(partner)
        return False

    @api.multi
    def name_get(self):
        return {
            this.id: '%s %s %s' % (
                this.this_partner_id.name,
                this.type_selection_id.name_get()[0][1],
                this.other_partner_id.name,
            )
            for this in self
        }

    @api.onchange('type_selection_id')
    def onchange_type_selection_id(self):
        """Add domain on other_partner_id according to category_other and
        contact_type_other"""
        domain = []
        if self.type_selection_id.contact_type_other:
            domain.append(
                ('is_company', '=',
                 self.type_selection_id.contact_type_other == 'c'))
        if self.type_selection_id.partner_category_other:
            domain.append(
                ('category_id', 'in',
                 self.type_selection_id.partner_category_other.ids))
        return {
            'domain': {
                'other_partner_id': domain,
            }
        }

    @api.onchange('this_partner_id')
    def onchange_this_partner_id(self):
        if not self.this_partner_id:
            return {'domain': {'type_selection_id': []}}
        return {
            'domain': {
                'type_selection_id': [
                    '|',
                    ('contact_type_this', '=', False),
                    ('contact_type_this', '=',
                     'c' if self.this_partner_id else 'p'),
                    '|',
                    ('partner_category_this', '=', False),
                    ('partner_category_this', 'in',
                     self.this_partner_id.category_id.ids),
                ],
            },
        }

    @api.one
    def write(self, vals):
        """divert non-problematic writes to underlying table"""
        underlying_objs = self._get_underlying_object()
        vals = {
            key: val
            for key, val in vals.iteritems()
            if not self._columns[key].readonly
        }
        vals['type_selection_id'] = vals.get(
            'type_selection_id',
            underlying_objs.type_selection_id.id
        )
        return underlying_objs.write(vals)

    @api.model
    def create(self, vals):
        """divert non-problematic creates to underlying table

        Create a res.partner.relation but return the converted id
        """
        vals = {
            key: val
            for key, val in vals.iteritems()
            if not self._columns[key].readonly
        }
        vals['type_selection_id'] = vals.get(
            'type_selection_id',
            False,
        )
        res = self.env[self._overlays].create(vals)
        return self.browse(res.id * PADDING)

    @api.one
    def unlink(self):
        """divert non-problematic creates to underlying table"""
        return self._get_underlying_object().unlink()
