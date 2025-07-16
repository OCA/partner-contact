# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestPartnerBankCode(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["res.bank"].search([]).write({"active": False})
        cls.bank1 = cls.env["res.bank"].create(
            {
                "name": "bank1",
                "bic": "some bic",
            }
        )
        cls.bank2 = cls.env["res.bank"].create(
            {
                "name": "bank2",
                "bic": "some bic",
                "bank_code": "4242",
            }
        )
        cls.bank3 = cls.env["res.bank"].create(
            {
                "name": "bank3",
                "bic": "some bic",
                "bank_code": "4242",
                "bank_branch_code": "434343",
            }
        )

    def test_name_get(self):
        self.assertEqual(self.bank1.display_name, "bank1 - some bic")
        self.assertEqual(self.bank2.display_name, "bank2 - some bic [4242]")
        self.assertEqual(self.bank3.display_name, "bank3 - some bic [4242/434343]")

    def test_name_search(self):
        # Search with name
        found_recs = self.env["res.bank"].name_search(name="some b")
        self.assertEqual(len(found_recs), 3)

        # Search with name equal only
        found_recs = self.env["res.bank"].name_search(name="some bic", operator="=")
        self.assertEqual(len(found_recs), 3)

        # Search with bank code
        found_recs = self.env["res.bank"].name_search(name="42")
        self.assertEqual(len(found_recs), 2)

        # Search with bank code not ilike
        # it should show 1 record because bank1, 2 don't have bank_branch_code
        found_recs = self.env["res.bank"].name_search(
            name="bank1", operator="not ilike"
        )
        self.assertEqual(len(found_recs), 1)

        # Search with bank branch code
        found_recs = self.env["res.bank"].name_search(name="43")
        self.assertEqual(len(found_recs), 1)
