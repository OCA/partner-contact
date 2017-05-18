# -*- coding: utf-8 -*-
# © 2017 Sunflower IT <http://sunflowerweb.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class PartnerMergeTestCase(TransactionCase):
    """Tests for Partner Merge"""

    def setUp(self):
        super(PartnerMergeTestCase, self).setUp()
        self.partner = self.env['res.partner']
        self.merge_wizard = \
            self.env['base.partner.merge.automatic.wizard']
        self.donald_domain = [('name', '=', 'Donald Duck')]
        self.mickey_domain = [('name', '=', 'Mickey Mouse')]

    def _unlink_all(self):
        self.partner.search(self.donald_domain).unlink()
        self.partner.search(self.mickey_domain).unlink()

    def _count_donalds_mickeys(self, donalds, mickeys):
        self.assertEquals(
            len(self.partner.search(self.donald_domain)), donalds)
        self.assertEquals(
            len(self.partner.search(self.mickey_domain)), mickeys)

    def _create_duplicates(self, field1, value1, field2, values2):
        for value2 in values2:
            self.partner.create({
                field1: value1,
                field2: value2,
            })

    def test_10_all_functionality(self):
        """ All functionality """

        # Create users with duplicate names
        self._unlink_all()
        self._create_duplicates('name', 'Donald Duck', 'email',
                                ['donald@therp.nl', 'donald@sunflowerweb.nl'])
        self._create_duplicates('name', 'Mickey Mouse', 'email',
                                ['mickey@therp.nl', 'mickey@sunflowerweb.nl'])
        # Test if there are two Donald Ducks and Mickey Mouses
        self._count_donalds_mickeys(2, 2)

        # Merge all names that start with 'D',
        self.partner.deduplicate_on_field('name',
                                          domain=[('name', 'like', 'D%')])
        # Test if there is one Donald but still two Mickeys
        self._count_donalds_mickeys(1, 2)

        # Create users with duplicate references
        self._unlink_all()
        self._create_duplicates('ref', 'DD123',
                                'name', ['Donald Duck', 'Mickey Mouse'])

        # Merge on reference, leaving out guys that have no ref
        self.partner.deduplicate_on_field('ref',
                                          domain=[('ref', '!=', False)])
        # Test if only one remains after
        self.assertEquals(len(self.partner.search([
            ('ref', '=', 'DD123')])), 1)
