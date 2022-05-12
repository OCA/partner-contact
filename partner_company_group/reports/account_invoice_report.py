# Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    company_group_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner Company Group",
        readonly=True,
    )

    def _select(self):
        res = super()._select()
        return f"{res}, partner.company_group_id"
