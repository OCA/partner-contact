# SDi
# Copyright 2018 David Juaneda - <djuaneda@sdi.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class TestResPartnerNav(TransactionCase):

    def setUp(self):
        super(TestResPartnerNav, self).setUp()

        res_partner = self.env['res.partner']
        self.parent = res_partner.browse(
            res_partner.name_create('IronShield')[0])

        self.child = res_partner.create({
            'name': 'Isen Hardearth',
            'street': 'Strongarm Avenue, 12',
            'parent_id': self.parent.id,
        })

    def test_open_commercial_partner(self):
        """ This test case checks
                - If the method redirects to the form view of the correct one
                of an object of the 'res.partner' class.
        """
        for child in self.parent.child_ids:
            action = child.open_commercial_partner()
            print("Child_id = {}".format(child.id))
            print("action.get('res_id') = {}".format(action.get('res_id')))
            self.assertEqual(child.id, action.get('res_id'),
                             'The contact ID from the partner must be equal to'
                             ' the ID of the contact to be displayed.')
