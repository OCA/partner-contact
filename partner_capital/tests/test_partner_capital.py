# Copyright 2015 Tecnativa - Antonio Espinosa
# Copyright 2015 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.base.tests.common import BaseCommon


class TestResPartner(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.currency_eur = cls.env.ref("base.EUR")
        cls.country_us = cls.env.ref("base.us")

        cls.turnover_range_1 = cls.env["res.partner.turnover_range"].create(
            {"name": "1M-10M"}
        )
        cls.turnover_range_2 = cls.env["res.partner.turnover_range"].create(
            {"name": "10M-50M"}
        )

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "capital_country_id": cls.country_us.id,
                "capital_amount": 1000000.00,
                "capital_currency_id": cls.currency_eur.id,
                "turnover_range_id": cls.turnover_range_1.id,
                "turnover_amount": 5000000.00,
                "company_size": "medium",
            }
        )

    def test_partner_fields(self):
        """Test ResPartner custom fields"""
        self.assertEqual(self.partner.capital_country_id, self.country_us)
        self.assertEqual(self.partner.capital_amount, 1000000.00)
        self.assertEqual(self.partner.capital_currency_id, self.currency_eur)
        self.assertEqual(self.partner.turnover_range_id, self.turnover_range_1)
        self.assertEqual(self.partner.turnover_amount, 5000000.00)
        self.assertEqual(self.partner.company_size, "medium")

    def test_turnover_range_fields(self):
        """Test ResPartnerTurnoverRange fields"""
        self.assertEqual(self.turnover_range_2.name, "10M-50M")
