# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.tests import common
from openerp.exceptions import ValidationError


class TestResPartnerEmailUnique(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestResPartnerEmailUnique, cls).setUpClass()
        partner_obj = (
            cls.env['res.partner']
               .with_context({'test_partner_email_unique': True})
        )
        cls.partner1 = partner_obj.create({
            'name': 'Partner1',
        })
        cls.partner2 = partner_obj.create({
            'name': 'Partner2',
        })

    def test_check_email(self):

        # Test can create/modify partners with different email
        self.partner1.email = 'same_email@test.com'
        self.partner2.email = 'different_email@test.com'
        self.assertNotEqual(self.partner1.email, self.partner2.email)
        self.partner2.ref = False

        # Test can't create/modify partner with same email
        with self.assertRaises(ValidationError):
            self.partner2.email = 'same_email@test.com'

        # Empty email addresses don't raise
        self.partner1.email = False
        self.partner2.email = False

    def test_copy_does_not_raise_duplicate_email_error(self):
        self.partner1.copy()
