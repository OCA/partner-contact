# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPartnerAddressDetails(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        ja = (
            cls.env["res.lang"]
            .with_context(active_test=False)
            .search([("code", "=", "ja_JP")])
        )
        cls.env["base.language.install"].create({"lang_ids": ja.ids}).lang_install()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Partner EN",
                "street": "317 Fairchild Dr",
                "city": "Fairfield",
                "zip": "94535",
                "country_id": cls.env.ref("base.us").id,
            }
        )
        cls.partner.partner_address_details = (
            "Partner EN\n" "317 Fairchild Dr\n" "Fairfield CA 94535\n" "United States"
        )
        cls.partner.with_context(lang="ja_JP").write(
            {
                "partner_address_details": (
                    "取引先（日本語）\n" "〒150-0001\n" "東京都渋谷区神宮前1-2-3\n" "日本"
                )
            }
        )

    def test_partner_report_address(self):
        # No is_report -> should NOT use partner_address_details
        res = self.partner.with_context(lang="ja_JP")._display_address()
        self.assertNotEqual(
            res.strip(),
            "取引先（日本語）\n〒150-0001\n東京都渋谷区神宮前1-2-3\n日本",
        )
        # is_report + en_US -> uses EN value
        res = self.partner.with_context(is_report=True, lang="en_US")._display_address()
        self.assertEqual(
            res.strip(),
            "Partner EN\n317 Fairchild Dr\nFairfield CA 94535\nUnited States",
        )
        # is_report + ja_JP -> uses JA translation
        res = self.partner.with_context(is_report=True, lang="ja_JP")._display_address()
        self.assertEqual(
            res.strip(),
            "取引先（日本語）\n〒150-0001\n東京都渋谷区神宮前1-2-3\n日本",
        )
