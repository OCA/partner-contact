# -*- coding: utf-8 -*-
# Copyright 2017-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Abstract model to show each relation from two sides."""
from psycopg2.extensions import AsIs

from odoo import api, fields, models
from odoo.tools import drop_view_if_exists


class ResPartnerRelationHierarchy(models.AbstractModel):
    """Abstract model to show each relation from two sides."""
    _auto = False
    _log_access = False
    _name = 'res.partner.relation.hierarchy'
    _description = 'Partners with all their partnes above'
    _order = 'partner_id, level desc, partner_above_id'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        required=True,
        readonly=True,
        help="The partner at the base of the hierarchy")
    partner_above_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner above',
        required=True,
        readonly=True,
        help="Partner somewhere above in the hierarchy")
    partner_below_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner below',
        required=True,
        readonly=True,
        help="Partner immediately below partner above in the hierarchy")
    level = fields.Integer(
        string='Level',
        required=True,
        readonly=True,
        help="Number of levels that partner above is higher up")
    hierarchy_display = fields.Char(
        string='Hierarchy',
        required=True,
        readonly=True,
        help="Compact representation of hierarchy")

    @api.model_cr_context
    def _auto_init(self):
        """Create hierarchy view only taking into account active relations.
        """
        cr = self._cr
        drop_view_if_exists(cr, self._table)
        cr.execute(
            """\
CREATE OR REPLACE VIEW %(table)s AS
WITH RECURSIVE hierarchy_relations AS (
    SELECT
        left_partner_id as partner_above_id,
        type_id,
        right_partner_id as partner_below_id,
        op.name as partner_above_name
     FROM res_partner_relation rpr
     JOIN res_partner_relation_type rt ON rpr.type_id = rt.id
     JOIN res_partner op ON left_partner_id = op.id
     WHERE rt.hierarchy = 'left'
      AND (rpr.date_start is NULL OR rpr.date_start <= CURRENT_DATE)
      AND (rpr.date_end is NULL OR rpr.date_end > CURRENT_DATE)
     UNION
     SELECT right_partner_id, type_id, left_partner_id, op.name
     FROM  res_partner_relation rpr
     JOIN  res_partner_relation_type rt ON rpr.type_id = rt.id
     JOIN res_partner op ON right_partner_id = op.id
     WHERE rt.hierarchy = 'right'
      AND (rpr.date_start is NULL OR rpr.date_start <= CURRENT_DATE)
      AND (rpr.date_end is NULL OR rpr.date_end > CURRENT_DATE)
 ),
 hierarchy_tree(
    partner_id, partner_above_id, partner_below_id, level, hierarchy_display,
    path, cycle
 ) AS (
     SELECT
        partner_below_id as partner_id, partner_above_id, partner_below_id,
        1 as level, partner_above_name as hierarchy_display,
        ARRAY[partner_below_id], false
     FROM hierarchy_relations hr
     UNION ALL
     SELECT htree.partner_id, hr.partner_above_id, hr.partner_below_id,
        htree.level + 1,
        hr.partner_above_name || '/' || htree.hierarchy_display,
        htree.path || hr.partner_below_id,
        hr.partner_below_id = ANY(htree.path)
     FROM hierarchy_relations hr, hierarchy_tree htree
     WHERE hr.partner_below_id = htree.partner_above_id
       AND NOT cycle
 )
 SELECT
    row_number() over (order by partner_id, level, partner_above_id) as id, *
 FROM hierarchy_tree ht
            """,
            {'table': AsIs(self._table)})
        return super(ResPartnerRelationHierarchy, self)._auto_init()
