# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestResPartnerIndustry(TransactionCase):
    def setUp(self):
        super(TestResPartnerIndustry, self).setUp()
        self.industry_1 = self.env.ref('base.res_partner_industry_O')
        self.industry_2 = self.env.ref('base.res_partner_industry_P')
        self.industry_3 = self.env.ref('base.res_partner_industry_Q')

    def test_res_partner_industry_complete_name(self):
        self.assertEqual(
            self.industry_1.complete_name, 'Public Administration'
        )
        self.industry_1.parent_id = self.industry_2
        self.assertEqual(
            self.industry_1.complete_name, 'Education / Public Administration'
        )
        self.industry_2.parent_id = self.industry_3
        self.assertEqual(
            self.industry_1.complete_name,
            'Health/Social / Education / Public Administration',
        )
