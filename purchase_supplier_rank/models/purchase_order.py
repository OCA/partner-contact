# Copyright 2021 ForgeFlow, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for record in res:
            partners = record.partner_id | record.partner_id.commercial_partner_id
            partners._increase_rank("supplier_rank")
        return res
