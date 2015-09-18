#    Author: Charbel Jacquin
#    Copyright 2015 Camptocamp SA
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

from openerp.tests import common
from openerp.exceptions import ValidationError


class TestPartnerRelation(common.TransactionCase):

    def setUp(self):

        super(TestPartnerRelation, self).setUp()

        self.partner_model = self.env['res.partner']
        self.relation_type_model = self.env['res.partner.relation.type']
        self.relation_model = self.env['res.partner.relation']

        self.partner_1 = self.partner_model.create({
            'name':  'Test User 1',
            'is_company': False
        })

        self.partner_2 = self.partner_model.create({
            'name': 'Test User 2',
            'is_company': False
        })

        self.relation_allow = self.relation_type_model.create({
            'name': 'allow',
            'name_inverse': 'allow_inverse',
            'contact_type_left': 'p',
            'contact_type_right': 'p',
            'allow_self': True
        })

        self.relation_disallow = self.relation_type_model.create({
            'name': 'disallow',
            'name_inverse': 'disallow_inverse',
            'contact_type_left': 'p',
            'contact_type_right': 'p',
            'allow_self': False
        })

        self.relation_default = self.relation_type_model.create({
            'name': 'default',
            'name_inverse': 'default_inverse',
            'contact_type_left': 'p',
            'contact_type_right': 'p',
        })

    def test_self_allowed(self):

        self.relation_model.create({'type_id': self.relation_allow.id,
                                    'left_partner_id': self.partner_1.id,
                                    'right_partner_id': self.partner_1.id})

    def test_self_disallowed(self):
        with self.assertRaises(ValidationError):
            self.relation_model.create({'type_id': self.relation_disallow.id,
                                        'left_partner_id': self.partner_1.id,
                                        'right_partner_id': self.partner_1.id})

    def test_self_default(self):
        with self.assertRaises(ValidationError):
            self.relation_model.create({'type_id': self.relation_default.id,
                                        'left_partner_id': self.partner_1.id,
                                        'right_partner_id': self.partner_1.id})
