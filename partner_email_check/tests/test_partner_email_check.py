# Copyright 2019 Komit <https://komit-consulting.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import Command
from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase


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

    def test_duplicate_per_company_scope_allows_other_company(self):
        """Under per-company scope the same email may be reused by a partner of
        another company."""
        self.disallow_duplicates()
        self.env.company.partner_email_check_duplicate_scope = "company"
        company_b = self.env["res.company"].create({"name": "Company B"})
        self.env["res.partner"].create(
            {
                "name": "company a partner",
                "email": "shared@domain.tld",
                "company_id": self.env.company.id,
            }
        )
        # Same email in another company is allowed under per-company scope.
        partner_b = self.env["res.partner"].create(
            {
                "name": "company b partner",
                "email": "shared@domain.tld",
                "company_id": company_b.id,
            }
        )
        self.assertEqual(partner_b.email, "shared@domain.tld")

    def test_duplicate_per_company_scope_blocks_same_company(self):
        """Per-company scope still blocks duplicates inside one company."""
        self.disallow_duplicates()
        self.env.company.partner_email_check_duplicate_scope = "company"
        self.env["res.partner"].create(
            {
                "name": "first",
                "email": "shared@domain.tld",
                "company_id": self.env.company.id,
            }
        )
        with self.assertRaises(UserError):
            self.env["res.partner"].create(
                {
                    "name": "second",
                    "email": "shared@domain.tld",
                    "company_id": self.env.company.id,
                }
            )

    def test_duplicate_global_scope_blocks_other_company(self):
        """Under global scope (default) the email must be unique across
        companies."""
        self.disallow_duplicates()
        self.assertEqual(self.env.company.partner_email_check_duplicate_scope, "global")
        company_b = self.env["res.company"].create({"name": "Company B"})
        self.env["res.partner"].create(
            {
                "name": "company a partner",
                "email": "shared@domain.tld",
                "company_id": self.env.company.id,
            }
        )
        with self.assertRaises(UserError):
            self.env["res.partner"].create(
                {
                    "name": "company b partner",
                    "email": "shared@domain.tld",
                    "company_id": company_b.id,
                }
            )

    def test_duplicate_in_inaccessible_record_disallowed(self):
        """A duplicate hidden from the user by record rules is still blocked,
        with a dedicated message that does not disclose the conflicting record.
        """
        self.disallow_duplicates()
        hidden_partner = self.env["res.partner"].create(
            {"name": "hidden", "email": "shared@domain.tld"}
        )
        # An internal user allowed to create partners (so creation does not
        # trip on unrelated access checks, e.g. base_partner_sequence reading
        # ir.sequence) but blocked from reading the conflicting record.
        groups = self.env.ref("base.group_user") | self.env.ref(
            "base.group_partner_manager"
        )
        restricted_user = self.env["res.users"].create(
            {
                "name": "Restricted",
                "login": "restricted_user",
                "group_ids": [Command.set(groups.ids)],
            }
        )
        # Global rule (no groups) so it applies to every non-superuser
        # regardless of the user's other groups; match by id to stay
        # independent of fields other modules may populate.
        self.env["ir.rule"].create(
            {
                "name": "Hide conflicting partner from everyone",
                "model_id": self.env.ref("base.model_res_partner").id,
                "groups": [Command.set([])],
                "domain_force": f"[('id', '!=', {hidden_partner.id})]",
            }
        )
        partner_model = self.env["res.partner"].with_user(restricted_user)
        # The restricted user cannot see the flagged partner ...
        self.assertFalse(partner_model.search([("email", "=", "shared@domain.tld")]))
        # ... but creating a duplicate is still blocked with the access message.
        with self.assertRaises(UserError) as catcher:
            partner_model.create({"name": "dup", "email": "shared@domain.tld"})
        self.assertIn("do not have access", str(catcher.exception))

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

    def test_invalid_email_addresses_allowed(self):
        self.env.company.partner_email_check_syntax = False
        self.test_partner.email = "bad@email@domain..com"
        self.assertTrue(self.test_partner.email)
