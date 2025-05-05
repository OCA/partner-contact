from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestResPartnerTelegramAlias(TransactionCase):
    def setUp(self):
        super().setUp()

        self.Partner = self.env["res.partner"]
        self.partner = self.Partner.create({"name": "Test Partner"})

    def test_create_strips_at_and_spaces(self):
        alias_raw = "  @my_alias  "
        partner2 = self.Partner.create(
            {
                "name": "Alias Create",
                "telegram_alias": alias_raw,
            }
        )
        self.assertEqual(partner2.telegram_alias, "my_alias")

    def test_write_strips_at_and_spaces(self):
        alias_raw = "  @anotherAlias  "
        self.partner.write({"telegram_alias": alias_raw})
        self.assertEqual(self.partner.telegram_alias, "anotherAlias")

    def test_invalid_alias_format(self):
        with self.assertRaises(ValidationError):
            self.partner.write({"telegram_alias": "a_b"})

        with self.assertRaises(ValidationError):
            self.partner.write({"telegram_alias": "invalid!alias"})

        long_alias = "a" * 33
        with self.assertRaises(ValidationError):
            self.partner.write({"telegram_alias": long_alias})

    def test_duplicate_alias(self):
        self.Partner.create({"name": "Partner One", "telegram_alias": "duplicate"})
        with self.assertRaises(ValidationError):
            self.Partner.create({"name": "Partner Two", "telegram_alias": "@Duplicate"})

    def test_allow_empty_alias(self):
        self.partner.write({"telegram_alias": False})
        self.assertFalse(self.partner.telegram_alias)
        self.partner.write({"telegram_alias": ""})
        self.assertEqual(self.partner.telegram_alias, "")
