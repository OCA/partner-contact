# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import Form, TransactionCase


class TestPhoneFormatOption(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.country_jp = cls.env.ref("base.jp")
        cls.country_us = cls.env.ref("base.us")
        cls.state_jp = cls.env.ref("base.state_jp_jp-13")
        cls.state_us = cls.env.ref("base.state_us_5")
        cls.company.country_id = cls.country_jp
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})

    def _set_phone_format(self, value):
        self.env["ir.config_parameter"].set_param(
            "phone_format_option.phone_format", value
        )

    def _format_phone(self, country, number, fname="phone"):
        """Set the partner country and phone number through the form, so that
        the onchange is triggered, and return the resulting value."""
        state = self.state_jp if country == self.country_jp else self.state_us
        with Form(self.partner) as form:
            form.country_id = country
            form.state_id = state
            form[fname] = number
            result = form[fname]
        return result

    def test_raw_is_not_reformatted(self):
        self._set_phone_format("RAW")
        result = self._format_phone(self.country_jp, "090-1234-5678")
        self.assertEqual(result, "090-1234-5678")

    def test_national_drops_country_code_for_same_country(self):
        self._set_phone_format("NATIONAL")
        result = self._format_phone(self.country_jp, "+81 90-1234-5678")
        self.assertFalse(result.startswith("+"))

    def test_national_keeps_country_code_for_other_country(self):
        self._set_phone_format("NATIONAL")
        result = self._format_phone(self.country_us, "+1 202-555-0143")
        self.assertTrue(result.startswith("+1"))

    def test_international_keeps_country_code(self):
        self._set_phone_format("INTERNATIONAL")
        result = self._format_phone(self.country_jp, "090-1234-5678")
        self.assertTrue(result.startswith("+81"))

    def test_mobile_is_formatted(self):
        self._set_phone_format("NATIONAL")
        result = self._format_phone(self.country_jp, "+81 90-1234-5678", fname="mobile")
        self.assertFalse(result.startswith("+"))
