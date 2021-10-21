# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import fields, models


class ResPartnerTitle(models.Model):
    _inherit = "res.partner.title"
    _order = "sequence, name"

    sequence = fields.Integer(default=10)
