# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.osv.expression import SQL_OPERATORS
from odoo.tools.sql import SQL


class ResPartner(models.Model):
    _inherit = "res.partner"

    properties_company_id = fields.Many2one(
        compute="_compute_properties_company_id",
        search="_search_properties_company_id",
        comodel_name="res.company",
    )
    properties_type_company = fields.Properties(
        definition="properties_company_id.partner_properties_definition_company",
        copy=True,
    )
    properties_type_person = fields.Properties(
        definition="properties_company_id.partner_properties_definition_person",
        copy=True,
    )

    @api.depends("company_id")
    @api.depends_context("company")
    def _compute_properties_company_id(self):
        for item in self:
            item.properties_company_id = item.company_id or self.env.company

    def _search_properties_company_id(self, operator, value):
        self.flush_model(["company_id"])
        query = self._where_calc([])
        query.add_where(
            SQL(
                "%s %s %s",
                self._field_to_sql(self._table, "properties_company_id", query),
                SQL_OPERATORS[operator],
                value,
            )
        )
        return [("id", "in", query)]

    def _field_to_sql(self, alias, fname, query=None, flush: bool = True) -> SQL:
        # OVERRIDE to allow to export the properties
        if fname == "properties_company_id":
            return SQL(
                """COALESCE(%(company_column)s, %(env_company)s)""",
                company_column=SQL.identifier(alias, "company_id"),
                env_company=self.env.company.id,
            )
        return super()._field_to_sql(alias, fname, query, flush)
