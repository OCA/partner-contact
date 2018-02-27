# © 2014-2016 Camptocamp SA
# @author: Nicolas Bessi
# © 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestStreet3(TransactionCase):

    def test_partner(self):
        # Test address_format has been updated on existing countries
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
        self.assertEqual(bart.street3, 'Tho')

        # test synchro of street3 on write
        homer.write({'street3': 'in OCA we trust'})
        self.assertEqual(bart.street3, 'in OCA we trust')
