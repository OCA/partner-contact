# -*- coding: utf-8 -*-
# Copyright 2014 Nicolas Bessi, Alexandre Fayolle, Camptocamp SA
# Copyright 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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
