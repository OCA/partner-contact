# Copyright 2019 Komit <https://komit-consulting.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase
from odoo.tools.misc import mute_logger


class TestPartnerEmailCheck(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.test_partner = cls.env["res.partner"].create({"name": "test"})
        cls.env.company.partner_email_check_syntax = True
        cls.env.company.partner_email_check_filter_duplicates = False
        cls.env.company.partner_email_check_check_deliverability = False

    def test_bad_email(self):
        """Test rejection of bad emails."""
        with self.assertRaises(ValidationError):
            self.test_partner.email = "bad@email@domain..com"

    def test_good_email(self):
        """Test acceptance of good"""
        self.test_partner.email = "goodemail@domain.com"
        self.assertTrue(self.test_partner.email)

    def test_bad_emails(self):
        """Test rejection of bad emails."""
        with self.assertRaises(ValidationError):
            self.test_partner.email = "good@domain.com,bad@email@domain..com"

    def test_good_emails(self):
        """Test acceptance of good"""
        self.test_partner.email = "goodemail@domain.com,goodemail2@domain.com"
        self.assertTrue(self.test_partner.email)

    def test_email_domain_normalization(self):
        """Test normalization of email domain names, including punycode."""
        self.test_partner.write({"email": "goodemail@xn--xamPle-9ua.com"})
        self.assertEqual(self.test_partner.email, "goodemail@éxample.com")

    def test_multi_email_domain_normalization(self):
        """Test normalization of email domain names of multiple addresses."""
        self.test_partner.write(
            {"email": "goodemail@doMAIN.com,othergood@xn--xample-9ua.com"}
        )
        self.assertEqual(
            self.test_partner.email, "goodemail@domain.com,othergood@éxample.com"
        )

    def test_email_local_normalization(self):
        """Test normalization of the local part of email addresses."""
        self.test_partner.write({"email": "Me@mail.org"})
        # .lower() is locale-dependent, so don't hardcode the result
        self.assertEqual(self.test_partner.email, "Me".lower() + "@mail.org")

    def test_multi_email_local_normalization(self):
        """Test normalization of the local part of multiple addresses."""
        self.test_partner.write({"email": "You@mAiL.net,mE@mail.com"})
        self.assertEqual(
            self.test_partner.email,
            "You".lower() + "@mail.net," + "mE".lower() + "@mail.com",
        )

    def disallow_duplicates(self):
        self.env.company.partner_email_check_filter_duplicates = True

    def test_duplicate_addresses_disallowed(self):
        self.disallow_duplicates()
        self.test_partner.write({"email": "email@domain.tld"})
        with self.assertRaises(UserError):
            self.env["res.partner"].create(
                {"name": "alsotest", "email": "email@domain.tld"}
            )

    def test_duplicate_after_normalization_addresses_disallowed(self):
        self.disallow_duplicates()
        self.env["res.partner"].create(
            {"name": "alsotest", "email": "email@doMAIN.tld"}
        )
        with self.assertRaises(UserError):
            self.test_partner.email = "email@domain.tld"

    def test_multiple_addresses_disallowed_when_duplicates_filtered(self):
        self.disallow_duplicates()
        with self.assertRaises(UserError):
            self.test_partner.email = "foo@bar.org,email@domain.tld"

    def test_duplicate_addresses_disallowed_copy_partner(self):
        self.disallow_duplicates()
        self.test_partner.write({"email": "email@domain.tld"})
        partner_copy = self.test_partner.copy()
        self.assertFalse(partner_copy.email)

    def test_duplicate_addresses_allowed_by_default(self):
        self.env["res.partner"].create(
            {"name": "alsotest", "email": "email@domain.tld"}
        )
        self.test_partner.email = "email@domain.tld"

    def check_deliverability(self):
        self.env.company.partner_email_check_check_deliverability = True

    def test_deliverable_addresses_allowed(self):
        self.check_deliverability()
        # We only need a resolving domain, not a real user
        self.test_partner.email = "gooddomain-icraglusrk@gmail.com"
        self.assertTrue(self.test_partner.email)

    def test_nondeliverable_addresses_not_allowed(self):
        self.check_deliverability()
        with self.assertRaises(ValidationError):
            # This domain may resolve by mistake on certain network setups
            # At least until a new version of email-validator is released
            # See https://github.com/JoshData/python-email-validator/pull/30
            self.test_partner.email = "cezrik@acoa.nrdkt"

    @mute_logger("odoo.addons.partner_email_check.models.res_partner")
    def test_lacking_dependency_does_not_halt_execution(self):
        with patch(
            "odoo.addons.partner_email_check.models.res_partner." "validate_email", None
        ):
            self.test_partner.email = "notatallvalid@@domain"

    @mute_logger("odoo.addons.partner_email_check.models.res_partner")
    def test_lacking_dependency_keeps_uniqueness_constraint_working(self):
        self.disallow_duplicates()
        with patch(
            "odoo.addons.partner_email_check.models.res_partner." "validate_email", None
        ):
            self.env["res.partner"].create(
                {"name": "alsotest", "email": "email@domain.tld"}
            )
            with self.assertRaises(UserError):
                self.test_partner.email = "email@domain.tld"

    def test_invalid_email_addresses_allowed(self):
        self.env.company.partner_email_check_syntax = False
        self.test_partner.email = "bad@email@domain..com"
        self.assertTrue(self.test_partner.email)
