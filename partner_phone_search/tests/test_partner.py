# Copyright 2018 - TODAY Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestResPartner(TransactionCase):

    def setUp(self):
        super(TestResPartner, self).setUp()
        self.PartnerObj = self.env['res.partner']
        self.partner_id = self.PartnerObj.create({
            'name': 'Serpent',
            'mobile': '1234567890',
            'email': 'abc.serpentcs@gmail.com',
            'customer': True,
            'city': 'india',
        })

    def test_name_search(self):
        partner_ids = self.PartnerObj.name_search(
            name="1234567890",
            operator='ilike',
            args=[('id', 'in', self.partner_id.ids)]
        )
        self.assertEqual(set([self.partner_id.id]),
                         set([a[0] for a in partner_ids]))
