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


class Base_Test_partner_category(TransactionCase):
    """
    Simple test creating a partner_category
    This is a base class for partner_category test cases.
    Inherit from this and setup values.
    """

    def setUp(self, vals=None):
        """
        Setting up partner_category.
        """
        if not vals:
            vals = {}
        # Default test values
        self.vals = {
            'name': 'This is a test partner_category name with unicödé',
            'active': True,
        }
        super(Base_Test_partner_category, self).setUp()
        # Create the parent
        partner_category_partner = self.registry('res.partner.category')
        self.vals['parent_id'] = partner_category_partner.create(
            self.cr, self.uid, {
                'name': 'Test parent',
                'active': True,
            }, context=None
        )

        self.vals = dict(self.vals.items() + vals.items())
        # Create the partner_category object; we will be testing this,
        # so store in self
        self.partner_category_id = partner_category_partner.create(
            self.cr, self.uid, self.vals, context=None
        )

    def test_partner_category(self):
        """
        Checking the partner_category creation.
        """
        partner_category = self.registry('res.partner.category')
        partner_category_obj = partner_category.browse(
            self.cr, self.uid, self.partner_category_id, context=None
        )
        for field in self.vals:
            val = partner_category_obj[field]
            if type(val) == browse_record:
                self.assertEquals(self.vals[field], val.id,
                                  "IDs for %s don't match: (%i != %i)" %
                                  (field, self.vals[field], val.id))
            else:
                self.assertEquals(ustr(self.vals[field]), ustr(val),
                                  "Values for %s don't match: (%s != %s)" %
                                  (field, ustr(self.vals[field]), ustr(val)))


class Test_partner_category_bad(Base_Test_partner_category):
    """
    Simple test creating a partner_category, test against bad values
    """
    def setUp(self):
        """
        Setting up partner_category, then changing the values to test against.
        """
        super(Test_partner_category_bad, self).setUp()
        # Change vals to something wrong
        self.vals = {'name': 'This is the wrong partner_category name',
                     'active': False,
                     }

    def test_partner_category(self):
        """
        Checking the partner_category creation, assertions should all be false.
        """
        partner_category_partner_category = self.registry(
            'res.partner.category'
        )
        partner_category_obj = partner_category_partner_category.browse(
            self.cr, self.uid, self.partner_category_id, context=None
        )
        for field in self.vals:
            val = partner_category_obj[field]
            if type(val) == browse_record:
                self.assertNotEqual(self.vals[field], val.id,
                                    "IDs for %s don't match: (%i != %i)" %
                                    (field, self.vals[field], val.id))
            else:
                self.assertNotEqual(ustr(self.vals[field]), ustr(val),
                                    "Values for %s don't match: (%s != %s)" %
                                    (field, ustr(self.vals[field]), ustr(val)))


class test_partner_category(TransactionCase):

    def setUp(self):
        super(test_partner_category, self).setUp()
        # Clean up registries
        self.registry('ir.model').clear_caches()
        self.registry('ir.model.data').clear_caches()
        # Get registries
        self.user_model = self.registry("res.users")
        self.partner_cat_model = self.registry("res.partner.category")
        # Get context
        self.context = self.user_model.context_get(self.cr, self.uid)
        # Create parent partner category
        self.test_parent_id = self.partner_cat_model.create(
            self.cr, self.uid, {
                'name': 'test_parent',
            }, context=self.context)

        self.test_child_id = self.partner_cat_model.create(
            self.cr, self.uid, {
                'name': 'test_child',
                'parent_id': self.test_parent_id,
            }, context=self.context)

        self.test_grandchild_id = self.partner_cat_model.create(
            self.cr, self.uid, {
                'name': 'test_grandchild',
                'parent_id': self.test_child_id,
            }, context=self.context)

        self.test_orphan_id = self.partner_cat_model.create(
            self.cr, self.uid, {
                'name': 'test_orphan',
            }, context=self.context)

    def test_name_search(self):

        self.assertItemsEqual(
            self.partner_cat_model.name_search(
                self.cr, self.uid, name='test_parent', context=self.context
            ),
            [
                (self.test_child_id, 'test_parent / test_child'),
                (self.test_grandchild_id,
                 'test_parent / test_child / test_grandchild'),
                (self.test_parent_id, 'test_parent'),
            ]
        )
        self.assertItemsEqual(
            self.partner_cat_model.name_search(
                self.cr, self.uid, name='test_child', context=self.context
            ),
            [
                (self.test_child_id, 'test_parent / test_child'),
                (self.test_grandchild_id,
                 'test_parent / test_child / test_grandchild'),
            ]
        )
        self.assertItemsEqual(
            self.partner_cat_model.name_search(
                self.cr, self.uid, name='test_grandchild', context=self.context
            ),
            [
                (self.test_grandchild_id,
                 'test_parent / test_child / test_grandchild'),
            ]
        )
        self.assertItemsEqual(
            self.partner_cat_model.name_search(
                self.cr, self.uid, name='test_orphan', context=self.context
            ),
            [
                (self.test_orphan_id, 'test_orphan'),
            ]
        )
