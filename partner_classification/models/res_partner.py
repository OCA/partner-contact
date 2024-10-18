# Copyright 2024 Trobz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_classification_id = fields.Many2one(
        "partner.classification", string="Partner Classification"
    )
