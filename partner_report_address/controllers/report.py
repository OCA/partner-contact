# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl

import json

from odoo import http

from odoo.addons.web.controllers import report


class ReportController(report.ReportController):
    @http.route(["/report/download"], type="http", auth="user")
    def report_download(self, data, context=None, token=None):
        is_str = isinstance(context, str)
        ctx = {}
        if isinstance(context, dict):
            ctx = context
        elif is_str and context:
            ctx = json.loads(context)
        ctx["is_report"] = True
        context = json.dumps(ctx) if is_str else ctx
        return super().report_download(data, context=context, token=token)
