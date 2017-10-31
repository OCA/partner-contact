# Copyright 2016-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


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
