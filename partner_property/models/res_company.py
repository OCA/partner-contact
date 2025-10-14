# Copyright 2024-2025 Tecnativa - Víctor Martínez
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

    @api.model
    def web_search_read(
        self, domain, specification, offset=0, limit=None, order=None, count_limit=None
    ):
        """Override the method to return the "appropriate" company if searched
        by any of the fields.
        This method is used to display the search fields (Add custom filter), the
        properties in the partners are multi-company, and the domain
        [("partner_properties_definition_company", "!=', False)] would return all
        the companies, in that case the data of the last company would be displayed,
        which would be totally confusing.
        Example:
        Existing companies: Company A + Company B + Company C
        Selected company: Company A
        Now it will show: Property custom (Company A).
        """
        f_names = [
            "partner_properties_definition_company",
            "partner_properties_definition_person",
        ]
        if any(dom[0] in f_names for dom in domain):
            domain = [("id", "=", self.env.company.id)]
        return super().web_search_read(
            domain,
            specification,
            offset=offset,
            limit=limit,
            order=order,
            count_limit=count_limit,
        )
