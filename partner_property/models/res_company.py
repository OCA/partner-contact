# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    partner_properties_definition_company = fields.PropertiesDefinition(
        string="Partner Properties (company)",
        compute="_compute_partner_properties_definition_company",
        inverse="_inverse_partner_properties_definition_company",
    )
    partner_properties_definition_person = fields.PropertiesDefinition(
        string="Partner Properties (person)",
        compute="_compute_partner_properties_definition_person",
        inverse="_inverse_partner_properties_definition_person",
    )

    @api.depends_context("company")
    def _compute_partner_properties_definition_company(self):
        ICP = self.env["ir.config_parameter"]
        value = ICP.sudo().get_param("partner_property.properties_definition_company")
        pt = fields.PropertiesDefinition()
        for item in self:
            item.partner_properties_definition_company = pt.convert_to_cache(
                value, item
            )

    @api.depends_context("company")
    def _compute_partner_properties_definition_person(self):
        ICP = self.env["ir.config_parameter"]
        value = ICP.sudo().get_param("partner_property.properties_definition_person")
        pt = fields.PropertiesDefinition()
        for item in self:
            item.partner_properties_definition_person = pt.convert_to_cache(value, item)

    def _inverse_partner_properties_definition_company(self):
        ICP = self.env["ir.config_parameter"]
        pt = fields.PropertiesDefinition()
        for item in self:
            value = pt.convert_to_column(
                item.partner_properties_definition_company, item
            )
            ICP.sudo().set_param(
                "partner_property.properties_definition_company", value
            )

    def _inverse_partner_properties_definition_person(self):
        ICP = self.env["ir.config_parameter"]
        pt = fields.PropertiesDefinition()
        for item in self:
            value = pt.convert_to_column(
                item.partner_properties_definition_person, item
            )
            ICP.sudo().set_param("partner_property.properties_definition_person", value)
