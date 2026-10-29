# Copyright 2025 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _phone_get_number_fields(self):
        # by default, it returns ['phone', 'mobile']
        # only return 'phone', otherwise when you update the 'mobile'
        # field, the 'phone' field is with the value of the mobile number!
        return ["phone"]
