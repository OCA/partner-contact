# Copyright 2020 Acsone SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    customer = fields.Boolean(
        string="Is a Customer",
        default=True,
        help="Check this box if this contact is a customer."
        "It can be selected in sales orders.",
    )
    supplier = fields.Boolean(
        string="Is a Vendor",
        help="Check this box if this contact is a vendor."
        "It can be selected in purchase orders.",
    )
