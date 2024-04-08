#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PartnerNameHistory(models.Model):
    _name = "partner.name.history"
    _description = "History of partner name"

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        ondelete="cascade",
        string="Partner",
        readonly=True,
        required=True,
    )
    old_name = fields.Char(
        readonly=True,
        required=True,
    )
    change_date = fields.Datetime(
        default=fields.Datetime.now,
        required=True,
    )
