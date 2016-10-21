# -*- coding: utf-8 -*-
# © 2014-2016 Camptocamp SA
# @author: Nicolas Bessi
# © 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestStreet3(TransactionCase):

    def test_partner(self):
        # Create a new country to test the default address format
        country = self.env['res.country'].create({
            'name': 'Donut Land',
            'code': 'DL',
            })
        self.assertEqual(
            country.address_format,
            ("%(street)s\n%(street2)s\n%(street3)s\n"
             "%(city)s %(state_code)s %(zip)s\n"
             "%(country_name)s")
        )

        homer = self.env['res.partner'].create({
            'name': 'Homer Simpson',
            'city': 'Springfield',
            'street': '742 Evergreen Terrace',
            'street2': 'Donut Lane',
            'street3': 'Tho',
            'country_id': country.id,
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
