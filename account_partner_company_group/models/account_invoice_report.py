# Copyright 2026 Roofing Industries Ltd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools import SQL


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    company_group_id = fields.Many2one(
        "res.partner", string="Company Group", readonly=True
    )

    _depends = {
        "account.move": ["company_group_id"],
    }

    @api.model
    def _select(self) -> SQL:
        return SQL("%s, %s", super()._select(), SQL("move.company_group_id"))
