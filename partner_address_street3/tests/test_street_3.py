# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Nicolas Bessi
#    Copyright 2014 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import openerp.tests.common as test_common


class TestStreet3(test_common.TransactionCase):

    def test_partner(self):
        part_model = self.registry('res.partner')
        country_model = self.registry('res.country')
        country_id = country_model.create(
            self.cr,
            self.uid,
            {
                'name': 'Donut Land',
                'code': 'DNL',
            }
        )

        self.assertTrue(country_id)

        create_data = {
            'name': 'Homer Simpson',
            'city': 'Springfield',
            'street': '742 Evergreen Terrace',
            'street2': 'Donut Lane',
            'street3': 'Tho',
            'country_id': country_id,
            'is_company': True
        }

        homer_id = part_model.create(
            self.cr,
            self.uid,
            create_data
        )

        homer = part_model.browse(
            self.cr,
            self.uid,
            homer_id,
        )

        self.assertEqual(
            homer.country_id.address_format,
            ("%(street)s\n%(street2)s\n%(street3)s\n"
             "%(city)s %(state_code)s %(zip)s\n"
             "%(country_name)s")
        )

        create_data = {
            'name': 'Bart Simpson',
            'is_company': False,
            'parent_id': homer.id,
            'use_parent_address': True
        }

        bart_id = part_model.create(
            self.cr,
            self.uid,
            create_data
        )

        bart = part_model.browse(
            self.cr,
            self.uid,
            bart_id,
        )

        self.assertTrue(bart.street3, 'Tho')
