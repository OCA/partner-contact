# Copyright 2024 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/LGPL-3.0)

from odoo import fields, models


class ResPartnerCategory(models.Model):
    _inherit = "res.partner.category"

    description = fields.Char(translate=True)
