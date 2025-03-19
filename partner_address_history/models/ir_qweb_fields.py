# Copyright 2025 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Contact(models.AbstractModel):
    _inherit = "ir.qweb.field.contact"

    @api.model
    def value_to_html(self, value, options):
        """Add date change to the report"""
        if not value:
            return ""

        date_change = fields.Date.from_string(self.env.context.get("date_change"))
        if self.env.company.keep_partner_history and date_change:
            value = value.sudo().with_context(date_change=date_change)
        return super().value_to_html(value, options)
