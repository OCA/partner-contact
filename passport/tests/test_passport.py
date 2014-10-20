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
from datetime import date


class Base_Test_passport(TransactionCase):
    """Simple test creating a passport
    This is a base class for passport test cases.
    Inherit from this and setup values.
    """

    def setUp(self, vals=None):
        """
        Setting up passport.
        """
        if vals is None:
            vals = {}
        # Default test values
        self.vals = {'name': 'This is a test passport name',
                     'number': 'A200124789',
                     'country_id': 1,
                     'expiration_date': date(2013, 11, 14),
                     'birth_date': date(1980, 11, 21),
                     'gender': 'male',
                     }
        super(Base_Test_passport, self).setUp()
        # Overwrite vals if needed
        self.vals = dict(self.vals.items() + vals.items())
        # Create the passport object; we will be testing this, so store in self
        res_passport = self.registry('res.passport')
        self.passport_id = res_passport.create(
            self.cr, self.uid, self.vals, context=None
        )

    def test_passport(self):
        """
        Checking the passport creation.
        """
        res_passport = self.registry('res.passport')
        passport_obj = res_passport.browse(
            self.cr, self.uid, self.passport_id, context=None
        )
        for field in self.vals:
            val = passport_obj[field]
            if type(val) == browse_record:
                self.assertEquals(self.vals[field], val.id,
                                  "IDs for %s don't match: (%i != %i)" %
                                  (field, self.vals[field], val.id))
            else:
                self.assertEquals(str(self.vals[field]), str(val),
                                  "Values for %s don't match: (%s != %s)" %
                                  (field, str(self.vals[field]), str(val)))


class Test_passport_bad(Base_Test_passport):
    """Simple test creating a passport, test against bad values"""

    def setUp(self):
        """
        Setting up passport, then changing the values to test against.
        """
        super(Test_passport_bad, self).setUp()
        # Change vals to something wrong
        self.vals = {
            'name': 'This is the wrong passport name',
            'number': 'A111111111',
            'country_id': 0,
            'expiration_date': date(1999, 11, 14),
            'birth_date': date(1999, 11, 21),
            'gender': '',
        }

    def test_passport(self):
        """
        Checking the passport creation, assertions should all be false.
        """
        res_passport = self.registry('res.passport')
        passport_obj = res_passport.browse(
            self.cr, self.uid, self.passport_id, context=None
        )
        for field in self.vals:
            val = passport_obj[field]
            if type(val) == browse_record:
                self.assertNotEqual(self.vals[field], val.id,
                                    "IDs for %s don't match: (%i != %i)" %
                                    (field, self.vals[field], val.id))
            else:
                self.assertNotEqual(str(self.vals[field]), str(val),
                                    "Values for %s don't match: (%s != %s)" %
                                    (field, str(self.vals[field]), str(val)))


class Test_passport_name_get(TransactionCase):
    """Test name_get"""

    def setUp(self):
        """
        Setting up passport with name, country, either and none.
        """
        super(Test_passport_name_get, self).setUp()
        res_passport = self.registry('res.passport')
        res_country = self.registry('res.country')
        country = res_country.browse(self.cr, self.uid, 1, context=None)
        self.name_on_passport = 'test name'
        self.country_name = country.name_get()[0][1]
        self.both = res_passport.create(
            self.cr, self.uid, {'name': self.name_on_passport,
                                'country_id': country.id, },
            context=None)
        self.name_only = res_passport.create(
            self.cr, self.uid, {'name': self.name_on_passport, },
            context=None)
        self.country_only = res_passport.create(
            self.cr, self.uid, {'country_id': country.id, },
            context=None)
        self.neither = res_passport.create(
            self.cr, self.uid, {},
            context=None)

    def test_passport(self):
        """
        Checking the passport creation, assertions should all be false.
        """
        res_passport = self.registry('res.passport')
        both_obj = res_passport.browse(
            self.cr, self.uid, self.both, context=None
        )
        name_only = res_passport.browse(
            self.cr, self.uid, self.name_only, context=None
        )
        country_only = res_passport.browse(
            self.cr, self.uid, self.country_only, context=None
        )
        neither = res_passport.browse(
            self.cr, self.uid, self.neither, context=None
        )
        self.assertEquals(
            both_obj.name_get()[0][1],
            ' | '.join((self.country_name, self.name_on_passport)),
            'Error in passport name_get() with both country name and name on '
            'passport.'
        )
        self.assertEquals(
            name_only.name_get()[0][1], self.name_on_passport,
            'Error in passport name_get() with only name on passport.'
        )
        self.assertEquals(
            country_only.name_get()[0][1], self.country_name,
            'Error in passport name_get() with only name of country.'
        )
        self.assertEquals(
            neither.name_get()[0][1], '',
            'Error in passport name_get() with neither country name nor name '
            'on passport.'
        )
