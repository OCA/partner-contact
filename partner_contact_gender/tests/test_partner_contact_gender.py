# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests.common import TransactionCase


class TestPartnerContactGender(TransactionCase):
    def setUp(self):
        super(TestPartnerContactGender, self).setUp()
        self.testpartner = self.env['res.partner'].create({
            'name': 'test',
            'title': self.env.ref('base.res_partner_title_madam').id,
        })

    def test_partner_contact_gender(self):
        from ..hooks import post_init_hook
        post_init_hook(self.cr, None)
        self.assertEqual(self.testpartner.gender, 'female')
