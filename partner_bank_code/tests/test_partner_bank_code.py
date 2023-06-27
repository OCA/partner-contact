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
        search = self.env["res.bank"].name_search
        self.assertItemsEqual(
            search("some b"),
            self.bank1.name_get() + self.bank2.name_get() + self.bank3.name_get(),
        )
        self.assertItemsEqual(
            search("42"), self.bank2.name_get() + self.bank3.name_get()
        )
        self.assertItemsEqual(search("43"), self.bank3.name_get())
        self.assertItemsEqual(search("bank3", limit=None), self.bank3.name_get())
