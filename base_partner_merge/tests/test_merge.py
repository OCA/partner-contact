# -*- coding: utf-8 -*-
# © 2017 Sunflower IT <http://sunflowerweb.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
from openerp.tests.common import TransactionCase

class PartnerMergeTestCase(TransactionCase):
    """Tests for Partner Merge"""

    def setUp(self):
        super(PartnerMergeTestCase, self).setUp()
        self.partner = self.env['res.partner']
        self.merge_wizard = \
            self.env['base.partner.merge.automatic.wizard']

    def test_10_all_functionality(self):
        # Delete all Donald Ducks
        donald_domain = [('name', '=', 'Donald Duck')]
        self.partner.search(donald_domain).unlink()

        # Create two partners called Donald Duck
        partner_donald = self.partner.create({
            'name': 'Donald Duck',
            'email': 'donald@sunflowerweb.nl',
        })
        partner_donald2 = self.partner.create({
            'name': 'Donald Duck',
            'email': 'donald@therp.nl',
        })

        # Test if there are two Donald Ducks
        donalds = self.partner.search(donald_domain)
        self.assertEquals(len(donalds), 2)

        # Merge them,
        wizard_id = self.merge_wizard.create({
            'group_by_name': True,
            'state': "option"
        })
        wizard_id.automatic_process_cb()

        # Test if there is now one Donald Duck
        donalds = self.partner.search(donald_domain)
        self.assertEquals(len(donalds), 1)

        # Delete all Donald Ducks
        self.partner.search(donald_domain).unlink()




