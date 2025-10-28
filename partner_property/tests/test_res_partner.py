# Copyright 2024 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestResPartnerProperty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_a = cls.env["res.company"].create(
            {
                "name": "Company A",
            }
        )
        cls.company_b = cls.env["res.company"].create(
            {
                "name": "Company B",
            }
        )

    # Test that properties_company_id is set correctly using the company in context.
    def test_properties_company_A(self):
        partner = (
            self.env["res.partner"]
            .with_company(self.company_a.id)
            .create(
                {
                    "name": "Partner Test with company A",
                }
            )
        )
        self.assertEqual(
            partner.properties_company_id,
            self.company_a,
        )

    def test_properties_company_B(self):
        partner = (
            self.env["res.partner"]
            .with_company(self.company_b.id)
            .create(
                {
                    "name": "Partner Test with company B",
                }
            )
        )
        self.assertEqual(
            partner.properties_company_id,
            self.company_b,
        )

    def test_properties_company_id(self):
        partner = self.env["res.partner"].create({"name": "Partner Test"})
        # The partner has no company set, so the properties_company_id should
        # always match the current context company.
        self.assertEqual(
            partner.with_company(self.company_a.id).properties_company_id,
            self.company_a,
        )
        self.assertEqual(
            partner.with_company(self.company_b.id).properties_company_id,
            self.company_b,
        )
        # Searching should also work..
        self.assertEqual(
            self.env["res.partner"]
            .with_company(self.company_a.id)
            .search(
                [
                    ("properties_company_id", "=", self.company_a.id),
                    ("id", "=", partner.id),
                ]
            ),
            partner,
        )
        self.assertEqual(
            self.env["res.partner"]
            .with_company(self.company_b.id)
            .search(
                [
                    ("properties_company_id", "=", self.company_b.id),
                    ("id", "=", partner.id),
                ]
            ),
            partner,
        )
        # Except if we set an explicit company.. then it should match that
        # company regardless of the context company.
        partner.company_id = self.company_a
        self.assertEqual(
            partner.with_company(self.company_a.id).properties_company_id,
            self.company_a,
        )
        self.assertEqual(
            partner.with_company(self.company_b.id).properties_company_id,
            self.company_a,
        )
        # Searching should also work..
        self.assertEqual(
            self.env["res.partner"]
            .with_company(self.company_a.id)
            .search(
                [
                    ("properties_company_id", "=", self.company_a.id),
                    ("id", "=", partner.id),
                ]
            ),
            partner,
        )
        self.assertFalse(
            self.env["res.partner"]
            .with_company(self.company_b.id)
            .search(
                [
                    ("properties_company_id", "=", self.company_b.id),
                    ("id", "=", partner.id),
                ]
            ),
            partner,
        )
