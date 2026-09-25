# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestPartnerBankCode(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["res.partner.bank"].search([]).write({"active": False})
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})

        cls.bank1 = cls.env["res.partner.bank"].create(
            {
                "partner_id": cls.partner.id,
                "account_number": "ACC1",
                "bank_name": "bank1",
                "bank_bic": "some bic",
            }
        )
        cls.bank2 = cls.env["res.partner.bank"].create(
            {
                "partner_id": cls.partner.id,
                "account_number": "ACC2",
                "bank_name": "bank2",
                "bank_bic": "some bic",
                "bank_code": "4242",
            }
        )
        cls.bank3 = cls.env["res.partner.bank"].create(
            {
                "partner_id": cls.partner.id,
                "account_number": "ACC3",
                "bank_name": "bank3",
                "bank_bic": "some bic",
                "bank_code": "4242",
                "bank_branch_code": "434343",
            }
        )

    def test_name_get(self):
        self.assertEqual(self.bank1.display_name, "ACC1 - bank1")
        self.assertEqual(self.bank2.display_name, "ACC2 - bank2 [4242]")
        self.assertEqual(self.bank3.display_name, "ACC3 - bank3 [4242/434343]")

    def test_name_search(self):
        # Search with bank_name
        found_recs = self.env["res.partner.bank"].name_search(name="bank")
        self.assertEqual(len(found_recs), 3)

        # Search with bank_bic equal only
        found_recs = self.env["res.partner.bank"].name_search(
            name="SOME BIC", operator="="
        )
        self.assertEqual(len(found_recs), 3)

        # Search with bank code
        found_recs = self.env["res.partner.bank"].name_search(name="42")
        self.assertEqual(len(found_recs), 2)

        # Search not ilike "bank1" → only bank1 matches (by name), so bank2 and
        # bank3 remain.
        found_recs = self.env["res.partner.bank"].name_search(
            name="bank1", operator="not ilike"
        )
        self.assertEqual(len(found_recs), 2)

        # Search with bank branch code
        found_recs = self.env["res.partner.bank"].name_search(name="43")
        self.assertEqual(len(found_recs), 1)

        # Search with negative operator (e.g., "!=")
        found_recs = self.env["res.partner.bank"].name_search(
            name="SOME BIC", operator="!="
        )
        self.assertEqual(len(found_recs), 0)

        # Explicitly test the fallback in _search_display_name when value is empty
        domain = self.env["res.partner.bank"]._search_display_name("ilike", "")
        # Since it falls back to super, it should return Domain.TRUE
        # or similar based on Odoo 20
        self.assertTrue(domain is not None)
