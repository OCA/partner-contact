# Copyright 2023 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    partner_ref_readonly = fields.Boolean(
        string="Partner Reference Readonly",
        help="If marked, the Reference in partners will not be editable.",
    )
    partner_generated_reference_unique = fields.Boolean(
        compute="_compute_partner_generated_reference_unique",
        inverse="_inverse_partner_generated_reference_unique",
        groups="base.group_system",
        help="This is a technical field that allows to get this from config parameter",
    )

    def _compute_partner_generated_reference_unique(self):
        """
        Compute the parameter to be accessible on company level
        """
        unique = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("base_partner_sequence.partner_generated_reference_unique")
        )
        self.partner_generated_reference_unique = unique

    def _inverse_partner_generated_reference_unique(self):
        """
        Allows to change the parameter through company field.
        """
        unique = bool()
        for company in self:
            unique = company.partner_generated_reference_unique
        self.env["ir.config_parameter"].sudo().set_param(
            "base_partner_sequence.partner_generated_reference_unique", unique
        )
