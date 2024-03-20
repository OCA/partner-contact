# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _get_rendering_context(self, report, docids, data):
        """Set context key to split partner address on two line only on report"""
        res = super()._get_rendering_context(report, docids, data)
        docs = res.get("docs")
        if docs:
            res["docs"] = docs.with_context(_two_lines_partner_address=True)
        return res
