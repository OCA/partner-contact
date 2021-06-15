# Copyright 2020 Tecnativa - Carlos Dauden
# Copyright 2020 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestPartnerContactAddressDefault(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.Partner = self.env["res.partner"]
        self.partner = self.Partner.create({"name": "Parent partner"})
        self.partner_child_delivery1 = self.Partner.create(
            {
                "name": "Child delivery 1",
                "type": "delivery",
                "parent_id": self.partner.id,
            }
        )
        self.partner_child_delivery2 = self.Partner.create(
            {
                "name": "Child delivery 2",
                "type": "delivery",
                "parent_id": self.partner.id,
            }
        )
        self.partner_child_invoice = self.Partner.create(
            {"name": "Child invoice", "type": "invoice", "parent_id": self.partner.id}
        )

    def test_contact_address_default(self):
        self.partner.partner_delivery_id = self.partner
        self.partner.partner_invoice_id = self.partner
        res = self.partner.address_get(["delivery", "invoice"])
        self.assertEqual(res["delivery"], self.partner.id)
        self.assertEqual(res["invoice"], self.partner.id)

        self.partner_child_delivery2.partner_delivery_id = self.partner_child_delivery2
        self.partner_child_delivery2.partner_invoice_id = self.partner_child_delivery2
        res = self.partner_child_delivery2.address_get(["delivery", "invoice"])
        self.assertEqual(res["delivery"], self.partner_child_delivery2.id)
        self.assertEqual(res["invoice"], self.partner_child_delivery2.id)
