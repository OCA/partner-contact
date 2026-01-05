# Copyright 2020 Tecnativa - Carlos Dauden
# Copyright 2020 Tecnativa - Sergio Teruel
# Copyright 2024 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.osv import expression


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_delivery_id = fields.Many2one(
        comodel_name="res.partner",
        string="Shipping address",
    )
    partner_invoice_id = fields.Many2one(
        comodel_name="res.partner",
        string="Invoice address",
    )
    partner_contact_id = fields.Many2one(
        comodel_name="res.partner",
        string="Default contact",
    )
    partner_delivery_domain = fields.Binary(compute="_compute_partner_domains")
    partner_invoice_domain = fields.Binary(compute="_compute_partner_domains")
    partner_contact_domain = fields.Binary(compute="_compute_partner_domains")

    @api.depends_context("company")
    @api.depends("commercial_partner_id")
    def _compute_partner_domains(self):
        company = self.env.company
        for partner in self:
            base_domain = [("id", "child_of", partner.commercial_partner_id.id)]
            if company.contact_shipping_address_delivery_partner_only:
                partner.partner_delivery_domain = expression.OR(
                    [
                        [("id", "=", partner.commercial_partner_id.id)],
                        expression.AND([base_domain, [("type", "=", "delivery")]]),
                    ]
                )
            elif company.contact_address_default_allow_all_partners:
                partner.partner_delivery_domain = []
            else:
                partner.partner_delivery_domain = expression.AND(
                    [base_domain, [("type", "=", "delivery")]]
                )
            if company.contact_address_default_allow_all_partners:
                partner.partner_invoice_domain = []
                partner.partner_contact_domain = []
                continue
            partner.partner_invoice_domain = expression.AND(
                [base_domain, [("type", "=", "invoice")]]
            )
            partner.partner_contact_domain = expression.AND(
                [base_domain, [("type", "=", "contact")]]
            )

    def get_address_default_type(self):
        """This will be the extension method for other contact types"""
        return ["delivery", "invoice", "contact"]

    def address_get(self, adr_pref=None):
        """Force the contact, delivery or invoice addresses. It will
        try to default to the one set in the commercial partner if any"""
        res = super().address_get(adr_pref)
        adr_pref = adr_pref or []
        default_address_type_list = {
            x for x in adr_pref if x in self.get_address_default_type()
        }
        for partner in self:
            for addr_type in default_address_type_list:
                default_address_id = (
                    partner[f"partner_{addr_type}_id"]
                    or partner.commercial_partner_id[f"partner_{addr_type}_id"]
                )
                if default_address_id:
                    res[addr_type] = default_address_id.id
        return res

    def write(self, vals):
        """We want to prevent archived contacts as default addresses"""
        if vals.get("active") is False:
            self.search([("partner_delivery_id", "in", self.ids)]).write(
                {"partner_delivery_id": False}
            )
            self.search([("partner_invoice_id", "in", self.ids)]).write(
                {"partner_invoice_id": False}
            )
            self.search([("partner_contact_id", "in", self.ids)]).write(
                {"partner_contact_id": False}
            )
        return super().write(vals)
