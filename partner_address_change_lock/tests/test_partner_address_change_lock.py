# Copyright 2026 Akretion (https://www.akretion.com).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestPartnerAddressLock(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "street": "1 Street OCA",
                "zip": "69001",
                "city": "Lyon",
                "country_id": cls.env.ref("base.fr").id,
            }
        )
        cls.contact = cls.env["res.partner"].create(
            {
                "name": "Test Contact",
                "parent_id": cls.partner.id,
                "street": "2 Street Odoo",
                "zip": "69002",
                "city": "Lyon",
                "country_id": cls.env.ref("base.fr").id,
            }
        )
        cls.journal = cls.env["account.journal"].search(
            [
                ("type", "=", "sale"),
                ("company_id", "=", cls.env.company.id),
            ],
            limit=1,
        )

    def _create_posted_invoice(self, partner, payment_state="not_paid"):
        invoice = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": partner.id,
                "journal_id": self.journal.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Service",
                            "quantity": 1,
                            "price_unit": 100.0,
                        },
                    )
                ],
            }
        )
        invoice.action_post()
        if payment_state == "paid":
            self.env["account.payment.register"].with_context(
                active_model="account.move",
                active_ids=invoice.ids,
            ).create({}).action_create_payments()
        return invoice

    def test_block_any_address_field_unpaid(self):
        self.env.company.partner_address_lock_mode = "any_address_field"
        self._create_posted_invoice(self.partner)
        for field, value in [
            ("street", "99 Street Bloquée"),
            ("zip", "75001"),
            ("city", "Paris"),
            ("country_id", self.env.ref("base.be").id),
        ]:
            with self.assertRaises(ValidationError):
                self.partner.write({field: value})
        self.partner.write({"name": "Test Partner Updated"})

    def test_block_country_only_mode(self):
        self.env.company.partner_address_lock_mode = "country"
        self._create_posted_invoice(self.partner)
        with self.assertRaises(ValidationError):
            self.partner.write({"country_id": self.env.ref("base.be").id})
        self.partner.write({"street": "Street Open"})
        self.assertEqual(self.partner.street, "Street Open")

    def test_allow_after_payment_and_child_contact_never_blocked(self):
        self.env.company.partner_address_lock_mode = "any_address_field"
        self._create_posted_invoice(self.partner, payment_state="paid")
        self.partner.write({"street": "Street Open"})
        self.assertEqual(self.partner.street, "Street Open")
        self._create_posted_invoice(self.partner)
        self.contact.write({"street": "Street Source"})
        self.assertEqual(self.contact.street, "Street Source")

    def test_address_history_html_any_address_field(self):
        self.env.company.partner_address_lock_mode = "any_address_field"
        self.assertFalse(self.contact.address_history_html)
        self.partner.write({"street": "2 Street Open Source"})
        self.assertIn("1 Street OCA", self.partner.address_history_html)
        self.partner.write({"street": "3 Street Open Source"})
        self.assertIn("1 Street OCA", self.partner.address_history_html)
        self.assertIn("2 Street Open Source", self.partner.address_history_html)
