# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class Animal(models.Model):
    _inherit = "animal"

    partner_id = fields.Many2one(
        "res.partner", string="Owner", index=True, tracking=True
    )
