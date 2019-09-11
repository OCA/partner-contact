# -*- coding: utf-8 -*-
# Copyright 2017 Komit <http://komit-consulting.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestPartnerEmailCheck(TransactionCase):
    def setUp(self):
        super(TestPartnerEmailCheck, self).setUp()
        self.test_partner = self.env['res.partner'].create({
            'name': 'test',
        })
        self.env['ir.config_parameter'].set_param(
            'partner_email_check_filter_duplicates', False
        )
        self.env['ir.config_parameter'].set_param(
            'partner_email_check_check_deliverability', False
        )

    def test_bad_email(self):
        """Test rejection of bad emails."""
        with self.assertRaises(ValidationError):
            self.test_partner.email = 'bad@email@domain..com'

    def test_good_email(self):
        """Test acceptance of good"""
        self.test_partner.email = 'goodemail@domain.com'
        self.assertTrue(self.test_partner.email)

    def test_bad_emails(self):
        """Test rejection of bad emails."""
        with self.assertRaises(ValidationError):
            self.test_partner.email = 'good@domain.com,bad@email@domain..com'

    def test_good_emails(self):
        """Test acceptance of good"""
        self.test_partner.email = 'goodemail@domain.com,goodemail2@domain.com'
        self.assertTrue(self.test_partner.email)

    def test_email_domain_normalization(self):
        """Test normalization of email domain names, including punycode."""
        self.test_partner.write({'email': 'goodemail@xn--xamPle-9ua.com'})
        self.assertEqual(self.test_partner.email, u'goodemail@éxample.com')

    def test_multi_email_domain_normalization(self):
        """Test normalization of email domain names of multiple addresses."""
        self.test_partner.write({
            'email': 'goodemail@doMAIN.com,othergood@xn--xample-9ua.com'
        })
        self.assertEqual(
            self.test_partner.email,
            u'goodemail@domain.com,othergood@éxample.com'
        )

    def test_email_local_normalization(self):
        """Test normalization of the local part of email addresses."""
        self.test_partner.write({'email': 'Me@mail.org'})
        # .lower() is locale-dependent, so don't hardcode the result
        self.assertEqual(self.test_partner.email, 'Me'.lower() + '@mail.org')

    def test_multi_email_local_normalization(self):
        """Test normalization of the local part of multiple addresses."""
        self.test_partner.write({'email': 'You@mAiL.net,mE@mail.com'})
        self.assertEqual(
            self.test_partner.email,
            'You'.lower() + '@mail.net,' + 'mE'.lower() + '@mail.com'
        )

    def disallow_duplicates(self):
        self.env['ir.config_parameter'].set_param(
            'partner_email_check_filter_duplicates', True
        )

    def test_duplicate_addresses_disallowed(self):
        self.disallow_duplicates()
        self.test_partner.write({'email': 'email@domain.tld'})
        with self.assertRaises(ValidationError):
            self.env['res.partner'].create({
                'name': 'alsotest',
                'email': 'email@domain.tld'
            })

    def test_duplicate_after_normalization_addresses_disallowed(self):
        self.disallow_duplicates()
        self.env['res.partner'].create({
            'name': 'alsotest',
            'email': 'email@doMAIN.tld'
        })
        with self.assertRaises(ValidationError):
            self.test_partner.email = 'email@domain.tld'

    def test_multiple_addresses_disallowed_when_duplicates_filtered(self):
        self.disallow_duplicates()
        with self.assertRaises(ValidationError):
            self.test_partner.email = 'foo@bar.org,email@domain.tld'

    def test_duplicate_addresses_allowed_by_default(self):
        self.env['res.partner'].create({
            'name': 'alsotest',
            'email': 'email@domain.tld',
        })
        self.test_partner.email = 'email@domain.tld'
