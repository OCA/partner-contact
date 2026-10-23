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
        partner.invalidate_recordset()  # Invalidate cache to force recomputation
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

    def test_search_properties_definition_fallback(self):
        keys = (
            "partner_property.properties_definition_company",
            "partner_property.properties_definition_person",
        )
        ICP = self.env["ir.config_parameter"].sudo()
        ICP.search([("key", "in", list(keys))]).unlink()
        Company = self.env["res.company"]

        # No definition stored: ("=", False) matches all, ("!=", False) matches none.
        self.assertTrue(
            Company.search([("partner_properties_definition_company", "=", False)])
        )
        self.assertTrue(
            Company.search([("partner_properties_definition_person", "=", False)])
        )
        self.assertFalse(
            Company.search([("partner_properties_definition_company", "!=", False)])
        )
        self.assertFalse(
            Company.search([("partner_properties_definition_person", "!=", False)])
        )

        # Definition stored: the matches flip.
        for key in keys:
            ICP.set_param(key, '[{"name":"x","type":"char","string":"X"}]')
        self.assertFalse(
            Company.search([("partner_properties_definition_company", "=", False)])
        )
        self.assertTrue(
            Company.search([("partner_properties_definition_company", "!=", False)])
        )

        # `in` / `not in` shape (post-optimizer normalisation) behaves the same.
        ICP.search([("key", "in", list(keys))]).unlink()
        self.assertTrue(
            Company.search([("partner_properties_definition_company", "in", (False,))])
        )
        self.assertFalse(
            Company.search(
                [("partner_properties_definition_company", "not in", (False,))]
            )
        )

    def test_definition_field_roundtrip_and_web_search(self):
        """Cover compute (read), inverse (write), and web_search_read override."""
        keys = (
            "partner_property.properties_definition_company",
            "partner_property.properties_definition_person",
        )
        ICP = self.env["ir.config_parameter"].sudo()
        ICP.search([("key", "in", list(keys))]).unlink()

        # Inverse: writing the field stores via ir.config_parameter.
        company = self.env.company
        definition = [{"name": "x", "type": "char", "string": "X"}]
        company.partner_properties_definition_company = definition
        company.partner_properties_definition_person = definition
        self.assertTrue(ICP.get_param(keys[0]))
        self.assertTrue(ICP.get_param(keys[1]))

        # Compute: reading the field hydrates from ir.config_parameter.
        company.invalidate_recordset()
        self.assertTrue(company.partner_properties_definition_company)
        self.assertTrue(company.partner_properties_definition_person)

        # web_search_read clamps a definition-field domain to env.company.
        Company = self.env["res.company"]
        result = Company.web_search_read(
            domain=[("partner_properties_definition_company", "!=", False)],
            specification={"id": {}},
        )
        self.assertEqual(result["length"], 1)
        self.assertEqual(result["records"][0]["id"], company.id)
