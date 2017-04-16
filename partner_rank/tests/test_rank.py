# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
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

from openerp.tests.common import TransactionCase
from openerp.osv.orm import browse_record


class Base_Test_rank(TransactionCase):
    """
    Simple test creating a rank
    This is a base class for rank test cases.
    Inherit from this and setup values.
    """

    def setUp(self, vals={}):
        """
        Setting up rank.
        """
        # Default test values
        self.vals = {'name': 'This is a test rank',
                     'priority': 1,
                     'description': 'Description for rank',
                     }
        super(Base_Test_rank, self).setUp()
        # Overwrite vals if needed
        self.vals = dict(self.vals.items() + vals.items())
        # Create the rank object; we will be testing this, so store in self
        res_rank = self.registry('res.rank')
        self.rank_id = res_rank.create(
            self.cr, self.uid, self.vals, context=None)

    def test_rank(self):
        """
        Checking the rank creation.
        """
        res_rank = self.registry('res.rank')
        rank_obj = res_rank.browse(
            self.cr, self.uid, self.rank_id, context=None)
        for field in self.vals:
            val = rank_obj[field]
            if type(val) == browse_record:
                self.assertEquals(self.vals[field], val.id,
                                  "IDs for %s don't match: (%i != %i)" %
                                  (field, self.vals[field], val.id))
            else:
                self.assertEquals(str(self.vals[field]), str(val),
                                  "Values for %s don't match: (%s != %s)" %
                                  (field, str(self.vals[field]), str(val)))
