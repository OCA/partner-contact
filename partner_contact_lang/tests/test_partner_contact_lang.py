# -*- coding: utf-8 -*-
# © 2016 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests import common


class TestPartnerContactLang(common.TransactionCase):
    def setUp(self):
        super(TestPartnerContactLang, self).setUp()
        self.ResPartner = self.env['res.partner']
        self.partner = self.ResPartner.create({
            'name': 'Partner test',
            'lang': 'en_US',
        })
        self.contact = self.ResPartner.create({
            'name': 'Contact test',
            'lang': False,
            'parent_id': self.partner.id,
        })

    def test_onchange_parent_id(self):
        self.contact.parent_id = False
        res = self.contact.onchange_address(False, self.partner.id)
        self.assertEqual(res.get('value', {}).get('lang'), 'en_US')

    def test_write_parent_lang(self):
        self.partner.lang = 'en_US'
        self.assertEqual(self.contact.lang, 'en_US')
