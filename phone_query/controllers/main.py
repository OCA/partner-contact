# Copyright 2025 Kencove - Mohamed Alkobrosli
#   (<http://www.savoirfairelinux.com>).

from odoo import http
from odoo.http import request


class DashboardController(http.Controller):
    @http.route("/queries/<string:number>", type="json", auth="user")
    def get_dashboard_data(self, number, **kw):
        if kw["model"] and kw["operator"] and number:
            partner = request.env[kw["model"]]
            domain = partner._search_phone_mobile_search(
                operator=kw["operator"], value=number
            )
            return {
                "domain": domain,
            }
        else:
            return [(1, "=", 0)]
