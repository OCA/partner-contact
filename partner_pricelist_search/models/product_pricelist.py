# Copyright 2021 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    def show_pricelist_partners(self):
        xmlid = "base.action_partner_form"
        action = self.env["ir.actions.act_window"]._for_xml_id(xmlid)
        action["domain"] = [("property_product_pricelist", "in", self.ids)]
        return action
