# Copyright 2020 Tecnativa - Carlos Dauden
# Copyright 2020 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_delivery_id = fields.Many2one(
        comodel_name="res.partner", string="Shipping address",
    )
    partner_invoice_id = fields.Many2one(
        comodel_name="res.partner", string="Invoice address",
    )

    def get_address_default_type(self):
        return ["delivery", "invoice"]

    def address_get(self, adr_pref=None):
        res = super().address_get(adr_pref)
        default_address_type_list = self.get_address_default_type()
        for partner in self:
            for addr_type in default_address_type_list:
                default_address_id = partner["partner_{}_id".format(addr_type)]
                if default_address_id:
                    res[addr_type] = default_address_id
        return res
