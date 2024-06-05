# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    partner_properties_definition = fields.PropertiesDefinition(
        string="Partner Properties",
        compute="_compute_partner_properties_definition",
        inverse="_inverse_partner_properties_definition",
    )

    @api.depends_context("company")
    def _compute_partner_properties_definition(self):
        ICP = self.env["ir.config_parameter"]
        value = ICP.sudo().get_param("partner_property.properties_definition")
        pt = fields.PropertiesDefinition()
        for item in self:
            item.partner_properties_definition = pt.convert_to_cache(value, item)

    def _inverse_partner_properties_definition(self):
        ICP = self.env["ir.config_parameter"]
        pt = fields.PropertiesDefinition()
        for item in self:
            value = pt.convert_to_column(item.partner_properties_definition, item)
            ICP.sudo().set_param("partner_property.properties_definition", value)
