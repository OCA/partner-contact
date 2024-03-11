# Copyright 2020 Tecnativa - Carlos Dauden
# Copyright 2020 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestPartnerContactAddressDefault(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Partner = cls.env["res.partner"]
        cls.partner = cls.Partner.create({"name": "Parent partner"})
        cls.partner_child_delivery1 = cls.Partner.create(
            {
                "name": "Child delivery 1",
                "type": "delivery",
                "parent_id": cls.partner.id,
            }
        )
        cls.partner_child_delivery2 = cls.Partner.create(
            {
                "name": "Child delivery 2",
                "type": "delivery",
                "parent_id": cls.partner.id,
            }
        )
        cls.partner_child_invoice = cls.Partner.create(
            {"name": "Child invoice", "type": "invoice", "parent_id": cls.partner.id}
        )
        cls.partner_child_contact = cls.Partner.create(
            {"name": "Child contact", "type": "contact", "parent_id": cls.partner.id}
        )

    def test_contact_address_default(self):
        self.partner.partner_delivery_id = self.partner
        self.partner.partner_invoice_id = self.partner
        self.partner.partner_contact_id = self.partner
        res = self.partner.address_get(["delivery", "invoice", "contact"])
        self.assertEqual(res["delivery"], self.partner.id)
        self.assertEqual(res["invoice"], self.partner.id)
        self.assertEqual(res["contact"], self.partner.id)

        self.partner_child_delivery2.partner_delivery_id = self.partner_child_delivery2
        self.partner_child_delivery2.partner_invoice_id = self.partner_child_delivery2
        self.partner_child_delivery2.partner_contact_id = self.partner_child_delivery2
        res = self.partner_child_delivery2.address_get(
            ["delivery", "invoice", "contact"]
        )
        self.assertEqual(res["delivery"], self.partner_child_delivery2.id)
        self.assertEqual(res["invoice"], self.partner_child_delivery2.id)
        self.assertEqual(res["contact"], self.partner_child_delivery2.id)

    def test_contact_address_archived(self):
        self.partner.partner_delivery_id = self.partner_child_delivery2
        self.partner.partner_invoice_id = self.partner_child_invoice
        self.partner.partner_contact_id = self.partner_child_contact
        self.partner_child_contact.write({"active": False})
        self.partner_child_invoice.write({"active": False})
        self.partner_child_delivery2.write({"active": False})
        res = self.partner.address_get(["delivery", "invoice", "contact"])
        # As partner_child_delivery2 is archived, even though it is set as
        # partner_delivery_id it should fall back to partner_child_delivery1 here:
        self.assertEqual(res["delivery"], self.partner_child_delivery1.id)
        self.assertEqual(res["invoice"], self.partner.id)
        self.assertEqual(res["contact"], self.partner.id)
