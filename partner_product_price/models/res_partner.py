from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def action_partner_product_price(self):
        # Return a unique database action so filters may be saved towards the action.
        return self.env["ir.actions.actions"]._for_xml_id(
            "partner_product_price.product_product_action_sell"
        )
