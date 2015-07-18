# -*- coding: utf-8 -*-
# Python source code encoding : https://www.python.org/dev/peps/pep-0263/
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2015 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Antonio Espinosa <antonioea@antiun.com>
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

from .base import BaseCase
from .. import exceptions as ex


class PartnerContactCase(BaseCase):
    def test_empty_names(self):
        """Create/update a contact with False/empty names."""
        with self.assertRaises(ex.EmptyNamesError):
            self.partner_contact_create(False, False)
            self.partner_contact_create(False, '')
            self.partner_contact_create('', False)
            self.partner_contact_create('', '')
            self.partner_contact_create('  ', '')
            self.partner_contact_create('', '   ')
            self.partner_contact_create('   ', '  ')
        self.changed = self.partner_contact_create(u"Lástnäme", u"Fírstnäme")
        with self.assertRaises(ex.EmptyNamesError):
            self.changed.write({'lastname': False, 'firstname': False})
            self.changed.write({'lastname': False, 'firstname': ''})
            self.changed.write({'lastname': '', 'firstname': False})
            self.changed.write({'lastname': '', 'firstname': ''})
            self.changed.write({'lastname': '  ', 'firstname': ''})
            self.changed.write({'lastname': '', 'firstname': '   '})
            self.changed.write({'lastname': '   ', 'firstname': '  '})

    def test_only_firstname(self):
        """Create/update a contact with only firstname."""
        cases = (
            (False, u"Fírstnäme", u"Chängéd"),
            ('', u"Fírstnäme", u"Chängéd"),
            (False, u"Fírstnäme1 Fírstnäme2", u"Chängéd1 Chängéd2"),
            ('', u"Fírstnäme1 Fírstnäme2", u"Chängéd1 Chängéd2"),
            (u"Lástnäme", u"Fírstnäme", False),
            (u"Lástnäme", u"Fírstnäme", ''),
        )
        for lastname, firstname, firstname_new in cases:
            self.changed = self.partner_contact_create(lastname, firstname)
            self.expect(lastname, firstname)
            self.changed.write({'firstname': firstname_new})
            self.expect(lastname, firstname_new)

    def test_only_lastname(self):
        """Create/update a contact with only lastname."""
        cases = (
            (False, u"Lástnäme", u"Chängéd"),
            ('', u"Lástnäme", u"Chängéd"),
            (False, u"Lástnäme1 Lástnäme2", u"Chängéd1 Chängéd2"),
            ('', u"Lástnäme1 Lástnäme2", u"Chängéd1 Chängéd2"),
            (u"Fírstnäme", u"Lástnäme", False),
            (u"Fírstnäme", u"Lástnäme", ''),
        )
        for firstname, lastname, lastname_new in cases:
            self.changed = self.partner_contact_create(lastname, firstname)
            self.expect(lastname, firstname)
            self.changed.write({'lastname': lastname_new})
            self.expect(lastname_new, firstname)

    def test_names(self):
        """Create/update a contact with firstnames and lastnames."""
        cases = (
            (u"Fírstnäme", u"Lástnäme",
             u"FírstnämeChängéd", u"LástnämeChängéd"),
            (u"Fírstnäme1 Fírstnäme2", u"Lástnäme",
             u"Fírstnäme1 Fírstnäme2Chängéd", u"LástnämeChängéd"),
            (u"Fírstnäme", u"Lástnäme1 Lástnäme2",
             u"FírstnämeChängéd", u"Lástnäme1 Lástnäme2Chängéd"),
            (u"Fírstnäme1 Fírstnäme2", u"Lástnäme1 Lástnäme2",
             u"Fírstnäme1 Fírstnäme2Chängéd", u"Lástnäme1 Lástnäme2Chängéd"),
        )
        for f, l, fn, ln in cases:
            self.changed = self.partner_contact_create(l, f)
            self.expect(l, f)
            self.changed.write({'lastname': ln, 'firstname': fn})
            self.expect(ln, fn)

    def test_whitespaces(self):
        """Create/update a contact with names with several whitespaces."""
        cases = (
            ("  F1   F2  ", "  L1   L2   ", u"F1 F2", u"L1 L2",
             "  C1   C2  ", "  D1   D2   ", u"C1 C2", u"D1 D2",),
            ("    ", "  L1   L2   ", u"", u"L1 L2",
             "  C1   C2  ", "     ", u"C1 C2", u"",),
            ("  F1   F2  ", "     ", u"F1 F2", u"",
             "    ", "  D1   D2   ", u"", u"D1 D2",),
        )
        for f, l, fc, lc, fn, ln, fnc, lnc in cases:
            self.changed = self.partner_contact_create(l, f)
            self.expect(lc, fc)
            self.changed.write({'lastname': ln, 'firstname': fn})
            self.expect(lnc, fnc)

    def test_copy(self):
        """Copy a contact."""
        cases = (
            (u"Fírstnäme", u"Lástnäme",
             u"Fírstnäme", u"Lástnäme (copy)"),
            (u"Fírstnäme1 Fírstnäme2", u"Lástnäme",
             u"Fírstnäme1 Fírstnäme2", u"Lástnäme (copy)"),
            ("", u"Lástnäme",
             u"", u"Lástnäme (copy)"),
            (False, u"Lástnäme",
             False, u"Lástnäme (copy)"),
            (u"Fírstnäme", u"",
             u"Fírstnäme", u"(copy)"),
            (u"Fírstnäme1 Fírstnäme2", "",
             u"Fírstnäme1 Fírstnäme2", u"(copy)"),
            (u"Fírstnäme1 Fírstnäme2", False,
             u"Fírstnäme1 Fírstnäme2", u"(copy)"),
        )
        for f, l, fc, lc in cases:
            self.partner_contact_create(l, f)
            self.expect(l, f)
            self.changed = self.original.with_context(lang="en_US").copy()
            self.expect(lc, fc)


class PartnerContactCaseInverse(PartnerContactCase):
    def partner_contact_create(self, lastname, firstname):
        super(PartnerContactCaseInverse, self).partner_contact_create(
            lastname, firstname)
        self.original.company_id.names_order = 'first_last'

    def expect(self, lastname, firstname, name=None):
        if firstname and lastname:
            name = u"%s %s" % (firstname, lastname)
            super(PartnerContactCaseInverse, self).expect(
                firstname, lastname, name)
        else:
            super(PartnerContactCaseInverse, self).expect(
                firstname, lastname)
