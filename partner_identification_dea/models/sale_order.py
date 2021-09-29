# Copyright (C) 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    dea_number_id = fields.Many2one(
        "res.partner.id_number", string="DEA license", index=True, ondelete="restrict"
    )

    @api.onchange("dea_number_id")
    def _onchange_dea_number_id(self):
        self.partner_id = self.dea_number_id.partner_id.id
