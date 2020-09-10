# Copyright 2016 Antonio Espinosa
# Copyright 2020 Tecnativa - João Marques
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    partner_ref_unique = fields.Selection(
        selection=[
            ("none", "None"),
            ("companies", "Only companies"),
            ("all", "All partners"),
        ],
        string="Unique partner reference for",
        default="none",
    )

    def write(self, vals):
        """Launch manually the constraint check in partners as current ORM
        doesn't trigger the constraint on related fields.
        """
        res = super().write(vals)
        if "partner_ref_unique" in vals:
            partners = (
                self.env["res.partner"]
                .with_context(active_test=False)
                .search([("company_id", "in", [False] + self.ids)])
            )
            partners._check_ref()
        return res
