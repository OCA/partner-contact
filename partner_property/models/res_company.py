# Copyright 2024-2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.fields import Domain


class ResCompany(models.Model):
    _inherit = "res.company"

    partner_properties_definition_company = fields.PropertiesDefinition(
        string="Partner Properties (company)",
        compute="_compute_partner_properties_definition_company",
        inverse="_inverse_partner_properties_definition_company",
        search="_search_partner_properties_definition_company",
    )
    partner_properties_definition_person = fields.PropertiesDefinition(
        string="Partner Properties (person)",
        compute="_compute_partner_properties_definition_person",
        inverse="_inverse_partner_properties_definition_person",
        search="_search_partner_properties_definition_person",
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

    def _search_partner_properties_definition_company(self, operator, value):
        return self._search_partner_properties_definition_fallback(
            "partner_property.properties_definition_company", operator, value
        )

    def _search_partner_properties_definition_person(self, operator, value):
        return self._search_partner_properties_definition_fallback(
            "partner_property.properties_definition_person", operator, value
        )

    def _search_partner_properties_definition_fallback(
        self, param_key, operator, value
    ):
        # The Domain optimizer can normalise ('field', '=', False) to
        # ('field', 'in', {False}) before reaching the search method, so accept
        # both shapes. Domain.TRUE is falsy in bool context (sentinel quirk),
        # so use a plain ternary, not `cond and Domain.TRUE or Domain.FALSE`.
        negate = operator in ("!=", "not in")
        stored = self.env["ir.config_parameter"].sudo().get_param(param_key)
        empty = not stored
        return Domain.TRUE if (empty ^ negate) else Domain.FALSE

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
