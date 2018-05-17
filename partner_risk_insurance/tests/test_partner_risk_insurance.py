# -*- coding: utf-8 -*-
# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestPartnerRiskInsurance(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestPartnerRiskInsurance, cls).setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Mr. Odoo',
        })

    def test_compute_credit(self):
        self.partner.company_credit_limit = 1000.0
        self.partner.insurance_credit_limit = 3000.0
        self.partner._onchage_insurance_credit_limit()
        self.assertEqual(self.partner.credit_limit, 4000.0)
        # Set credit limit manually:
        self.partner.credit_limit = 1500.0
        self.assertEqual(self.partner.credit_limit, 1500.0)
