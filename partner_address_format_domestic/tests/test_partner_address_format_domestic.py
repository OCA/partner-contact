# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestPartnerAddressFormatDomestic(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country_us = cls.env["res.country"].search([("code", "=", "US")], limit=1)
        cls.country_jp = cls.env["res.country"].search([("code", "=", "JP")], limit=1)
        cls.country_us.address_format = "%(state_code)s\n%(zip)s\n%(country_name)s"
        cls.country_us.address_format_domestic = "%(state_code)s\n%(zip)s"
        cls.country_jp.address_format = "%(zip)s\n%(state_code)s\n%(country_name)s"
        cls.country_jp.address_format_domestic = "%(zip)s\n%(state_code)s"
        cls.company_us = cls.env["res.company"].create(
            {"name": "Test Company", "country_id": cls.country_us.id}
        )
        cls.partner_us = cls.env["res.partner"].create(
            {"name": "John Doe", "country_id": cls.country_us.id}
        )
        cls.partner_jp = cls.env["res.partner"].create(
            {"name": "Yamada Taro", "country_id": cls.country_jp.id}
        )
        cls.env.company = cls.company_us

    def test_us_partner_uses_domestic_format(self):
        format_us = self.partner_us._get_address_format()
        self.assertEqual(format_us, "%(state_code)s\n%(zip)s")

    def test_jp_partner_uses_default_format(self):
        format_jp = self.partner_jp._get_address_format()
        self.assertEqual(format_jp, "%(zip)s\n%(state_code)s\n%(country_name)s")
