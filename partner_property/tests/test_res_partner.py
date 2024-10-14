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
