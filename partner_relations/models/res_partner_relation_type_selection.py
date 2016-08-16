# -*- coding: utf-8 -*-
# © 2014-2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
'''
Created on 23 may 2014

@author: Ronald Portier, Therp

rportier@therp.nl
http://www.therp.nl

For the model defined here _auto is set to False to prevent creating a
database file. All i/o operations are overridden to use a sql SELECT that
takes data from res_partner_connection_type where each type is included in the
result set twice, so it appears that the connection type and the inverse
type are separate records..

The original function _auto_init is still called because this function
normally (if _auto == True) not only creates the db tables, but it also takes
care of registering all fields in ir_model_fields. This is needed to make
the field labels translatable.

example content for last lines of _statement:
select id, record_type,
  customer_id, customer_name, customer_city, customer_zip, customer_street,
  caller_id, caller_name, caller_phone, caller_fax, caller_email
from FULL_LIST as ResPartnerRelationTypeSelection where record_type = 'c'
ORDER BY ResPartnerRelationTypeSelection.customer_name asc,
ResPartnerRelationTypeSelection.caller_name asc;

'''
from psycopg2.extensions import AsIs
from openerp import api, fields, models
from openerp.tools import drop_view_if_exists
from .res_partner_relation_type import ResPartnerRelationType
from .res_partner import PADDING


class ResPartnerRelationTypeSelection(models.Model):
    '''Virtual relation types'''
    _name = 'res.partner.relation.type.selection'
    _description = 'All relation types'
    _auto = False  # Do not try to create table in _auto_init(..)
    _foreign_keys = []
    _log_access = False
    _order = 'name asc'

    _RECORD_TYPES = [
        ('a', 'Type'),
        ('b', 'Inverse type'),
    ]

    record_type = fields.Selection(_RECORD_TYPES, 'Record type')
    type_id = fields.Many2one('res.partner.relation.type', 'Type')
    name = fields.Char('Name')
    contact_type_this = fields.Selection(
        ResPartnerRelationType._get_partner_types.im_func,
        'Current record\'s partner type')
    contact_type_other = fields.Selection(
        ResPartnerRelationType._get_partner_types.im_func,
        'Other record\'s partner type')
    partner_category_this = fields.Many2one(
        'res.partner.category', 'Current record\'s category')
    partner_category_other = fields.Many2one(
        'res.partner.category', 'Other record\'s category')

    def _auto_init(self, cr, context=None):
        drop_view_if_exists(cr, self._table)
        cr.execute(
            '''create or replace view %(table)s as
            select
                id * %(padding)s as id,
                id as type_id,
                cast('a' as char(1)) as record_type,
                name as name,
                contact_type_left as contact_type_this,
                contact_type_right as contact_type_other,
                partner_category_left as partner_category_this,
                partner_category_right as partner_category_other
            from %(underlying_table)s
            union select
                id * %(padding)s + 1,
                id,
                cast('b' as char(1)),
                name_inverse,
                contact_type_right,
                contact_type_left,
                partner_category_right,
                partner_category_left
             from %(underlying_table)s''',
            {
                'table': AsIs(self._table),
                'padding': PADDING,
                'underlying_table': AsIs('res_partner_relation_type'),
            })

        return super(ResPartnerRelationTypeSelection, self)._auto_init(
            cr, context=context)

    @api.multi
    def name_get(self):
        """translate name using translations from res.partner.relation.type"""
        ir_translation = self.env['ir.translation']
        return [
            (
                this.id,
                ir_translation._get_source(
                    'res.partner.relation.type,name_inverse'
                    if this.get_type_from_selection_id()[1]
                    else 'res.partner.relation.type,name',
                    ('model',),
                    self.env.context.get('lang'),
                    this.name,
                    this.type_id.id
                )
            )
            for this in self
        ]

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """search for translated names in res.partner.relation.type"""
        res_partner_relation_type = self.env['res.partner.relation.type']
        relations = res_partner_relation_type.search([
            ('name', operator, name)
        ])
        inverse_relations = res_partner_relation_type.search([
            ('name_inverse', operator, name),
            ('symmetric', '=', False),
        ])
        return self.search(
            [
                (
                    'id', 'in',
                    map(lambda x: x * PADDING, relations.ids) +
                    map(lambda x: x * PADDING + 1, inverse_relations.ids)
                ),
            ] + (args or []),
            limit=limit
        ).name_get()

    @api.multi
    def get_type_from_selection_id(self):
        """Selection id ic computed from id of underlying type and the
        kind of record. This function does the inverse computation to give
        back the original type id, and about the record type."""
        type_id = self.id / PADDING
        is_reverse = (self.id % PADDING) > 0
        return type_id, is_reverse
