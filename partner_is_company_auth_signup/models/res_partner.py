# Copyright 2025 Sylvain LE GAL (GRAP)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _signup_retrieve_info(self, token):
        res = super()._signup_retrieve_info(token)
        if not res:
            return res

        partner = self._get_partner_from_token(token)
        res["company_type"] = partner.is_company and "company" or "person"
        return res
