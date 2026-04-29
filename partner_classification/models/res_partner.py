# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    classification_id = fields.Many2one(
        "res.partner.classification",
        string="Classification",
        tracking=True,
        check_company=True,
    )

    def _commercial_fields(self):
        return super()._commercial_fields() + ["classification_id"]
