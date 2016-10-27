# -*- coding: utf-8 -*-
# Copyright 2014 Nicolas Bessi, Alexandre Fayolle, Camptocamp SA
# Copyright 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import openerp.tests.common as test_common
from ..hooks import uninstall_hook


class TestStreet3(test_common.TransactionCase):

    def test_partner(self):
        """"Test address_format has been updated on existing countries"""
        us_country = self.env.ref('base.us')

        self.assertTrue('%(street3)s' in us_country.address_format)

        homer = self.env['res.partner'].create({
            'name': 'Homer Simpson',
            'city': 'Springfield',
            'street': '742 Evergreen Terrace',
            'street2': 'Donut Lane',
            'street3': 'Tho',
            'country_id': us_country.id,
        })

        # test synchro of street3 on create
        bart = self.env['res.partner'].create({
            'name': 'Bart Simpson',
            'parent_id': homer.id,
            'type': 'contact',
        })
        self.assertEquals(bart.street3, 'Tho')

        # test synchro of street3 on write
        homer.write({'street3': 'in OCA we trust'})
        self.assertEquals(bart.street3, 'in OCA we trust')

    def test_uninstall_hook(self):
        """"Test uninstall_hook"""
        us_country = self.env.ref('base.us')
        self.assertTrue('%(street3)s' in us_country.address_format)
        uninstall_hook(self.cr, self.registry)
        us_country.invalidate_cache()
        self.assertTrue('%(street3)s' not in us_country.address_format)
