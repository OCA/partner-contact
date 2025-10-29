# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestPartnerEnforceIban(TransactionCase):
    """Test enforcing IBAN validation for partner bank accounts."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Bank = cls.env["res.partner.bank"]
        cls.Config = cls.env["ir.config_parameter"].sudo()
        cls.Country = cls.env["res.country"]

        # Test data
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.partner_us = cls.env["res.partner"].create(
            {"name": "US Partner", "country_id": cls.env.ref("base.us").id}
        )
        cls.partner_de = cls.env["res.partner"].create(
            {"name": "German Partner", "country_id": cls.env.ref("base.de").id}
        )
        cls.partner_fr = cls.env["res.partner"].create(
            {"name": "French Partner", "country_id": cls.env.ref("base.fr").id}
        )

        # Test banks with countries
        cls.bank_de = cls.env["res.bank"].create(
            {
                "name": "German Bank",
                "bic": "DEUTDEFF",
                "country": cls.env.ref("base.de").id,
            }
        )
        cls.bank_fr = cls.env["res.bank"].create(
            {
                "name": "French Bank",
                "bic": "BNPAFRPP",
                "country": cls.env.ref("base.fr").id,
            }
        )
        cls.bank_us = cls.env["res.bank"].create(
            {
                "name": "US Bank",
                "bic": "BOFAUS3N",
                "country": cls.env.ref("base.us").id,
            }
        )

        # Test IBANs
        cls.valid_iban_gb = "GB82WEST12345698765432"  # UK IBAN
        cls.valid_iban_de = "DE89370400440532013000"  # German IBAN
        cls.valid_iban_fr = "FR1420041010050500013M02606"  # French IBAN
        cls.invalid_iban = "INVALID123"
        cls.invalid_iban_de = "DE12INVALIDIBAN1234567890"  # Invalid German IBAN

    def _set_enforcement(self, value):
        """Enable or disable strict IBAN validation."""
        self.Config.set_param(
            "partner_enforce_iban_validation.raise_exception", str(value).lower()
        )

    def _set_country_restrictions(
        self, bank_country_ids=None, partner_country_ids=None
    ):
        """Set country restrictions for validation."""
        if bank_country_ids is not None:
            country_str = ",".join(str(x) for x in bank_country_ids)
            self.Config.set_param(
                "partner_enforce_iban_validation.bank_country_ids",
                country_str,
            )
        if partner_country_ids is not None:
            country_str = ",".join(str(x) for x in partner_country_ids)
            self.Config.set_param(
                "partner_enforce_iban_validation.partner_country_ids",
                country_str,
            )

    def test_01_create_valid_iban_with_enforcement(self):
        """Should create record successfully if IBAN is valid and enforcement is ON."""
        self._set_enforcement(True)
        self._set_country_restrictions(bank_country_ids=[], partner_country_ids=[])
        bank = self.Bank.create(
            {
                "acc_number": self.valid_iban_gb,
                "partner_id": self.partner.id,
            }
        )
        self.assertEqual(bank.acc_number.replace(" ", ""), self.valid_iban_gb)

    def test_02_create_invalid_iban_with_enforcement(self):
        """Should raise ValidationError if IBAN is invalid and enforcement is ON."""
        self._set_enforcement(True)
        self._set_country_restrictions(bank_country_ids=[], partner_country_ids=[])
        with self.assertRaises(ValidationError):
            self.Bank.create(
                {
                    "acc_number": self.invalid_iban,
                    "partner_id": self.partner.id,
                    "bank_id": self.bank_de.id,
                }
            )

    def test_03_create_invalid_iban_without_enforcement(self):
        """Should NOT raise error if enforcement is OFF."""
        self._set_enforcement(False)
        self._set_country_restrictions(bank_country_ids=[], partner_country_ids=[])
        bank = self.Bank.create(
            {
                "acc_number": self.invalid_iban,
                "partner_id": self.partner.id,
            }
        )
        self.assertTrue(bank)

    def test_04_skip_validation_via_context(self):
        """Should skip validation if skip_iban_validation=True in context."""
        self._set_enforcement(True)
        self._set_country_restrictions(bank_country_ids=[], partner_country_ids=[])
        bank = self.Bank.with_context(skip_iban_validation=True).create(
            {
                "acc_number": self.invalid_iban,
                "partner_id": self.partner.id,
            }
        )
        self.assertTrue(bank)

    def test_05_country_filter_bank_country(self):
        """Should validate only when bank country matches."""
        self._set_enforcement(True)
        de_country_id = self.env.ref("base.de").id
        self._set_country_restrictions(bank_country_ids=[de_country_id])

        bank = self.Bank.create(
            {
                "acc_number": self.valid_iban_de,
                "bank_id": self.bank_de.id,
                "partner_id": self.partner.id,
            }
        )
        self.assertTrue(bank)

        bank2 = self.Bank.create(
            {
                "acc_number": self.invalid_iban,
                "partner_id": self.partner.id,
            }
        )
        self.assertTrue(bank2)

        bank3 = self.Bank.create(
            {
                "acc_number": self.invalid_iban + "_X",
                "bank_id": self.bank_us.id,
                "partner_id": self.partner.id,
            }
        )
        self.assertTrue(bank3)

    def test_06_country_filter_partner_country(self):
        """Should validate only when partner country matches."""
        self._set_enforcement(True)
        de_country_id = self.env.ref("base.de").id
        self._set_country_restrictions(partner_country_ids=[de_country_id])

        with self.assertRaises(ValidationError):
            self.Bank.create(
                {
                    "acc_number": self.invalid_iban_de,
                    "partner_id": self.partner_de.id,
                }
            )

        bank = self.Bank.create(
            {
                "acc_number": self.invalid_iban,
                "partner_id": self.partner_us.id,
            }
        )
        self.assertTrue(bank)

        bank3 = self.Bank.create(
            {"acc_number": self.invalid_iban + "2", "partner_id": self.partner_us.id}
        )
        self.assertTrue(bank3)

    def test_07_country_filter_both_countries(self):
        """Should validate when either bank OR partner country matches."""
        self._set_enforcement(True)
        de_country_id = self.env.ref("base.de").id
        self._set_country_restrictions(
            bank_country_ids=[de_country_id], partner_country_ids=[de_country_id]
        )

        bank1 = self.Bank.create(
            {
                "acc_number": self.valid_iban_de,
                "bank_id": self.bank_de.id,
                "partner_id": self.partner_us.id,
            }
        )
        self.assertTrue(bank1)

        bank2 = self.Bank.create(
            {
                "acc_number": self.valid_iban_de,
                "partner_id": self.partner_de.id,
            }
        )
        self.assertTrue(bank2)

    def test_08_no_country_restrictions(self):
        """Should validate IBAN-supporting countries when no country restrictions."""
        self._set_enforcement(True)
        self._set_country_restrictions(bank_country_ids=[], partner_country_ids=[])

        with self.assertRaises(ValidationError):
            self.Bank.create(
                {
                    "acc_number": self.invalid_iban,
                    "partner_id": self.partner.id,
                    "bank_id": self.bank_de.id,
                }
            )

        bank = self.Bank.create(
            {
                "acc_number": self.invalid_iban,
                "bank_id": self.bank_us.id,
                "partner_id": self.partner.id,
            }
        )
        self.assertTrue(bank)

    def test_09_empty_country_restrictions(self):
        """Validate IBAN-supporting countries when country restrictions are empty."""
        self._set_enforcement(True)
        self.Config.set_param("partner_enforce_iban_validation.bank_country_ids", "")
        self.Config.set_param("partner_enforce_iban_validation.partner_country_ids", "")

        with self.assertRaises(ValidationError):
            self.Bank.create(
                {
                    "acc_number": self.invalid_iban,
                    "partner_id": self.partner.id,
                    "bank_id": self.bank_de.id,
                }
            )

        bank = self.Bank.create(
            {
                "acc_number": self.invalid_iban,
                "bank_id": self.bank_us.id,
                "partner_id": self.partner.id,
            }
        )
        self.assertTrue(bank)

    def test_10_write_invalid_iban_with_enforcement(self):
        """Should raise ValidationError when updating to invalid IBAN."""
        self._set_enforcement(True)
        self._set_country_restrictions(bank_country_ids=[], partner_country_ids=[])

        bank = self.Bank.create(
            {
                "acc_number": self.valid_iban_de,
                "partner_id": self.partner.id,
                "bank_id": self.bank_de.id,
            }
        )

        with self.assertRaises(ValidationError):
            bank.write({"acc_number": self.invalid_iban})

    def test_11_write_valid_iban_with_enforcement(self):
        """Should successfully update to valid IBAN."""
        self._set_enforcement(True)
        bank = self.Bank.create(
            {
                "acc_number": self.valid_iban_gb,
                "partner_id": self.partner.id,
            }
        )

        bank.write({"acc_number": self.valid_iban_de})
        self.assertEqual(bank.acc_number.replace(" ", ""), self.valid_iban_de)

    def test_12_write_with_country_filter(self):
        """Should validate on write when country filters match."""
        self._set_enforcement(True)
        de_country_id = self.env.ref("base.de").id
        self._set_country_restrictions(partner_country_ids=[de_country_id])

        bank = self.Bank.create(
            {
                "acc_number": self.valid_iban_de,
                "partner_id": self.partner_de.id,
            }
        )

        with self.assertRaises(ValidationError):
            bank.write({"acc_number": self.invalid_iban_de})

    def test_13_parse_country_ids_with_garbage(self):
        """Should skip non-numeric and empty entries in country ID list."""
        self.Config.set_param(
            "partner_enforce_iban_validation.bank_country_ids", "12,,abc, ,34"
        )
        settings = self.env["res.config.settings"]
        ids = settings._load_iban_check_country_ids(self.env, "bank_country_ids")
        self.assertEqual(ids, [12, 34])

    def test_14_config_get_and_set_values(self):
        """Should correctly get/set IBAN config settings."""
        settings = self.env["res.config.settings"].create(
            {
                "raise_exception_on_invalid_iban": True,
                "iban_bank_country_ids": [(6, 0, [self.env.ref("base.de").id])],
                "iban_partner_country_ids": [(6, 0, [self.env.ref("base.us").id])],
            }
        )
        settings.set_values()

        new_settings = self.env["res.config.settings"].get_values()
        self.assertIn("iban_bank_country_ids", new_settings)
        self.assertIn("iban_partner_country_ids", new_settings)

    def test_15_empty_acc_number_skips_validation(self):
        """Should skip validation if acc_number is empty."""
        self._set_enforcement(True)
        self._set_country_restrictions(bank_country_ids=[], partner_country_ids=[])

        bank = self.Bank.create(
            {
                "acc_number": "",
                "partner_id": self.partner.id,
            }
        )
        self.assertEqual(bank.acc_number, "")

    def test_16_country_code_mismatch_bank(self):
        """Should raise error when IBAN country doesn't match bank country."""
        self._set_enforcement(True)
        fr_country_id = self.env.ref("base.fr").id
        self._set_country_restrictions(bank_country_ids=[fr_country_id])

        # French bank + German IBAN = error
        with self.assertRaises(ValidationError):
            self.Bank.create(
                {
                    "acc_number": self.valid_iban_de,
                    "bank_id": self.bank_fr.id,
                    "partner_id": self.partner.id,
                }
            )

    def test_17_country_code_mismatch_partner(self):
        """Should raise error when IBAN country doesn't match partner country."""
        self._set_enforcement(True)
        de_country_id = self.env.ref("base.de").id
        self._set_country_restrictions(partner_country_ids=[de_country_id])

        # German partner + French IBAN = error
        with self.assertRaises(ValidationError):
            self.Bank.create(
                {
                    "acc_number": self.valid_iban_fr,
                    "partner_id": self.partner_de.id,
                }
            )

    def test_18_non_iban_country_skip_validation(self):
        """Should skip validation for countries that don't support IBAN."""
        self._set_enforcement(True)
        us_country_id = self.env.ref("base.us").id
        self._set_country_restrictions(bank_country_ids=[us_country_id])

        # US bank + any IBAN = allowed (US doesn't support IBAN)
        bank = self.Bank.create(
            {
                "acc_number": self.valid_iban_de,
                "bank_id": self.bank_us.id,
                "partner_id": self.partner.id,
            }
        )
        self.assertTrue(bank)

    def test_19_country_code_match_success(self):
        """Should succeed when IBAN country matches bank/partner country."""
        self._set_enforcement(True)
        de_country_id = self.env.ref("base.de").id
        self._set_country_restrictions(bank_country_ids=[de_country_id])

        # German bank + German IBAN = success
        bank = self.Bank.create(
            {
                "acc_number": self.valid_iban_de,
                "bank_id": self.bank_de.id,
                "partner_id": self.partner.id,
            }
        )
        self.assertTrue(bank)

    def test_20_country_code_validation_no_filters(self):
        """Should validate country code only for IBAN-supporting countries."""
        self._set_enforcement(True)
        self._set_country_restrictions(bank_country_ids=[], partner_country_ids=[])

        # French bank + German IBAN = error (country mismatch)
        with self.assertRaises(ValidationError):
            self.Bank.create(
                {
                    "acc_number": self.valid_iban_de,
                    "bank_id": self.bank_fr.id,
                    "partner_id": self.partner.id,
                }
            )

        bank = self.Bank.create(
            {
                "acc_number": self.valid_iban_de,
                "bank_id": self.bank_us.id,
                "partner_id": self.partner.id,
            }
        )
        self.assertTrue(bank)

        bank2 = self.Bank.create(
            {
                "acc_number": self.valid_iban_gb,
                "partner_id": self.partner.id,
            }
        )
        self.assertTrue(bank2)
