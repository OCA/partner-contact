# -*- coding: utf-8 -*-
# © 2014-2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""
For the model defined here _auto is set to False to prevent creating a
database file. The model is based on a SQL view based on
res_partner_relation_type where each type is included in the
result set twice, so it appears that the connection type and the inverse
type are separate records..

The original function _auto_init is still called because this function
normally (if _auto == True) not only creates the db tables, but it also takes
care of registering all fields in ir_model_fields. This is needed to make
the field labels translatable.
"""
from psycopg2.extensions import AsIs

from openerp import api, fields, models
from openerp.tools import drop_view_if_exists

from .res_partner_relation_type import ResPartnerRelationType


PADDING = 10


class ResPartnerRelationTypeSelection(models.Model):
    """Virtual relation types"""
    _name = 'res.partner.relation.type.selection'
    _description = 'All relation types'
    _auto = False  # Do not try to create table in _auto_init(..)
    _foreign_keys = []
    _log_access = False
    _order = 'name asc'

    type_id = fields.Many2one(
        comodel_name='res.partner.relation.type',
        string='Type',
    )
    name = fields.Char('Name')
    contact_type_this = fields.Selection(
        selection=ResPartnerRelationType.get_partner_types.im_func,
        string='Current record\'s partner type',
    )
    is_inverse = fields.Boolean(
        string="Is reverse type?",
        help="Inverse relations are from right to left partner.",
    )
    contact_type_other = fields.Selection(
        selection=ResPartnerRelationType.get_partner_types.im_func,
        string='Other record\'s partner type',
    )
    partner_category_this = fields.Many2one(
        comodel_name='res.partner.category',
        string='Current record\'s category',
    )
    partner_category_other = fields.Many2one(
        comodel_name='res.partner.category',
        string='Other record\'s category',
    )
    allow_self = fields.Boolean(
        string='Reflexive',
    )
    is_symmetric = fields.Boolean(
        string='Symmetric',
    )

    @api.model_cr_context
    def _auto_init(self):
        cr = self._cr
        drop_view_if_exists(cr, self._table)
        cr.execute(
            """CREATE OR REPLACE VIEW %(table)s AS
            SELECT
                id * %(padding)s AS id,
                id AS type_id,
                name AS name,
                False AS is_inverse,
                contact_type_left AS contact_type_this,
                contact_type_right AS contact_type_other,
                partner_category_left AS partner_category_this,
                partner_category_right AS partner_category_other,
                allow_self,
                is_symmetric
            FROM %(underlying_table)s
            UNION SELECT
                id * %(padding)s + 1,
                id,
                name_inverse,
                True,
                contact_type_right,
                contact_type_left,
                partner_category_right,
                partner_category_left,
                allow_self,
                is_symmetric
             FROM %(underlying_table)s
             WHERE not is_symmetric
            """,
            {
                'table': AsIs(self._table),
                'padding': PADDING,
                'underlying_table': AsIs('res_partner_relation_type'),
            })
        return super(ResPartnerRelationTypeSelection, self)._auto_init()

    @api.multi
    def name_get(self):
        """Get name or name_inverse from underlying model."""
        return [
            (this.id,
             this.is_inverse and this.type_id.name_inverse or
             this.type_id.display_name)
            for this in self
        ]

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """Search for name or inverse name in underlying model."""
        # pylint: disable=no-value-for-parameter
        return self.search(
            [
                '|',
                ('type_id.name', operator, name),
                ('type_id.name_inverse', operator, name),
            ] + (args or []),
            limit=limit
        ).name_get()
