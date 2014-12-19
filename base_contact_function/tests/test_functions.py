# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Savoir-faire Linux
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
from openerp.tools import ustr


class Base_Test_function(TransactionCase):
    """
    Simple test creating a function
    This is a base class for function test cases.
    Inherit from this and setup values.
    """

    def setUp(self, vals=None):
        """
        Setting up function.
        """
        if not vals:
            vals = {}
        # Default test values
        self.vals = {
            'name': u'This is a test function name with uniödé',
            'acronym': u'This is a test function acronym with uniödé',
        }
        super(Base_Test_function, self).setUp()
        self.vals = dict(self.vals.items() + vals.items())
        # Create the function object; we will be testing this, so store in self
        function_pool = self.registry('res.partner.function')
        self.function_id = function_pool.create(
            self.cr, self.uid, self.vals, context=None
        )

    def test_function(self):
        """
        Checking the function creation.
        """
        function_function = self.registry('res.partner.function')
        function_obj = function_function.browse(
            self.cr, self.uid, self.function_id, context=None
        )
        for field in self.vals:
            val = function_obj[field]
            if type(val) == browse_record:
                self.assertEquals(self.vals[field], val.id,
                                  "IDs for %s don't match: (%i != %i)" %
                                  (field, self.vals[field], val.id))
            else:
                self.assertEquals(ustr(self.vals[field]), ustr(val),
                                  "Values for %s don't match: (%s != %s)" %
                                  (field, ustr(self.vals[field]), ustr(val)))


class Test_function_bad(Base_Test_function):
    """
    Simple test creating a function, test against bad values
    """
    def setUp(self):
        """
        Setting up function, then changing the values to test against.
        """
        super(Test_function_bad, self).setUp()
        # Change vals to something wrong
        self.vals = {'name': 'This is the wrong function name',
                     'acronym': 'This is the wrong function acronym',
                     }

    def test_function(self):
        """
        Checking the function creation, assertions should all be false.
        """
        function_function = self.registry('res.partner.function')
        function_obj = function_function.browse(
            self.cr, self.uid, self.function_id, context=None
        )
        for field in self.vals:
            val = function_obj[field]
            if type(val) == browse_record:
                self.assertNotEqual(self.vals[field], val.id,
                                    "IDs for %s don't match: (%i != %i)" %
                                    (field, self.vals[field], val.id))
            else:
                self.assertNotEqual(ustr(self.vals[field]), ustr(val),
                                    "Values for %s don't match: (%s != %s)" %
                                    (field, ustr(self.vals[field]), ustr(val)))
