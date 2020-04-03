# Copyright 2020 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    partner_invoice_id = fields.Many2one(domain="[('id', 'child_of', partner_id)]",)
    partner_shipping_id = fields.Many2one(domain="[('id', 'child_of', partner_id)]",)
