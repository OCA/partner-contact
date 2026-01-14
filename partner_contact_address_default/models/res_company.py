# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    contact_address_default_allow_all_partners = fields.Boolean()
    contact_shipping_address_delivery_partner_only = fields.Boolean()
