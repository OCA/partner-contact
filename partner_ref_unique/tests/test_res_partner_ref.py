# -*- coding: utf-8 -*-
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests import common
from openerp.exceptions import ValidationError


class TestResPartnerRefUnique(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestResPartnerRefUnique, cls).setUpClass()
        cls.company = cls.env.ref('base.main_company')
        partner_obj = cls.env['res.partner']
        cls.partner1 = partner_obj.create({
            'name': 'Partner1',
        })
        cls.partner2 = partner_obj.create({
            'name': 'Partner2',
        })

    def test_check_ref(self):
        # Test can create/modify partners with same ref
        self.company.partner_ref_unique = 'none'
        self.partner1.ref = 'same_ref'
        self.partner2.ref = 'same_ref'
        self.assertEqual(self.partner1.ref, self.partner2.ref)
        self.partner2.ref = False

        # Test can't create/modify partner with same ref
        self.company.partner_ref_unique = 'all'
        with self.assertRaises(ValidationError):
            self.partner2.ref = 'same_ref'

        # Test can't create/modify companies with same ref
        self.company.partner_ref_unique = 'companies'
        self.partner2.ref = 'same_ref'
        self.assertEqual(self.partner1.ref, self.partner2.ref)
        self.partner2.ref = False
        self.partner1.is_company = True
        self.partner2.is_company = True
        with self.assertRaises(ValidationError):
            self.partner2.ref = 'same_ref'
