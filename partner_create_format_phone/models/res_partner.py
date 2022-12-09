# Copyright 2022 Ooops Ashish Hirpara  <https://ooops404.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        res._onchange_mobile_validation()
        res._onchange_phone_validation()
        return res
