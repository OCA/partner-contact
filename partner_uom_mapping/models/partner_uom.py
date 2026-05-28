# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PartnerUom(models.Model):
    _name = "partner.uom"
    _description = "Partner Uom"

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        required=True,
        ondelete="cascade",
    )
    uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Unit of Measure",
        required=True,
        ondelete="cascade",
    )
    partner_uom = fields.Char(
        string="Partner Unit of Measure",
        required=True,
    )
    active = fields.Boolean(
        default=True,
    )

    @api.depends("partner_id.name", "partner_uom", "uom_id.name")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"{rec.partner_id.name} ({rec.partner_uom} > {rec.uom_id.name})"
            )

    _unique_partner_uom = models.Constraint(
        "EXCLUDE (partner_id WITH =, uom_id WITH =, partner_uom WITH =) "
        "WHERE (active=True)",
        "Only one active partner unit of measure with the same value can be active.",
    )
