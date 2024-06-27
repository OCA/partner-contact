# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    properties_company_id = fields.Many2one(
        compute="_compute_properties_company_id",
        comodel_name="res.company",
    )
    properties = fields.Properties(
        definition="properties_company_id.partner_properties_definition",
        copy=True,
    )

    @api.depends("company_id")
    @api.depends_context("company")
    def _compute_properties_company_id(self):
        for item in self:
            item.properties_company_id = item.company_id or self.env.company
