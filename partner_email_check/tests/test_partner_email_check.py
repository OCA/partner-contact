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
            'title': self.env.ref('base.res_partner_title_madam').id,
        })

    def test_bad_email(self):
        """Test rejection of bad emails."""
        with self.assertRaises(ValidationError):
            self.test_partner.email = 'bad@email@domain..com'

    def test_good_email(self):
        """Test acceptance of good"""
        self.test_partner.email = 'goodemail@domain.com'
        self.assertTrue(self.test_partner.email)
