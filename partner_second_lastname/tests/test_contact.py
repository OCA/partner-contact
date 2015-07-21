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
from openerp.addons.partner_firstname import exceptions as ex


class PartnerContactCase(BaseCase):
    def test_empty_names(self):
        """Create/update a contact with False/empty names."""
        cases = (
            (False, False, False),
            (False, '', False),
            (False, '   ', False),
            (False, False, ''),
            (False, '', ''),
            (False, '   ', ''),
            ('', False, False),
            ('', '', False),
            ('', '  ', False),
            ('', False, ''),
            ('', '', ''),
            ('', ' ', ''),
            ('  ', False, ''),
            ('  ', '', ''),
            ('  ', '    ', ''),
            ('', False, '   '),
            ('', '', '   '),
            ('', '  ', '   '),
            ('   ', False, '  '),
            ('   ', '', '  '),
            ('   ', '   ', '  '),
        )
        with self.assertRaises(ex.EmptyNamesError):
            for l, ls, f in cases:
                self.next_case()
                self.partner_contact_create(l, ls, f)
        self.changed = self.partner_contact_create(
            u"Lástnäme", u"LástnämeSécönd", u"Fírstnäme")
        with self.assertRaises(ex.EmptyNamesError):
            for l, ls, f in cases:
                self.next_case()
                self.changed.write({
                    'lastname': l, 'lastname_second': ls, 'firstname': f})

    def test_only_firstname(self):
        """Create/update a contact with only firstname."""
        cases = (
            (False, False, u"Fírstnäme", u"Chängéd"),
            (False, '', u"Fírstnäme", u"Chängéd"),
            ('', False, u"Fírstnäme", u"Chängéd"),
            ('', '', u"Fírstnäme", u"Chängéd"),
            (False, False, u"Fírstnäme1 Fírstnäme2", u"Chängéd1 Chängéd2"),
            (False, '', u"Fírstnäme1 Fírstnäme2", u"Chängéd1 Chängéd2"),
            ('', False, u"Fírstnäme1 Fírstnäme2", u"Chängéd1 Chängéd2"),
            ('', '', u"Fírstnäme1 Fírstnäme2", u"Chängéd1 Chängéd2"),
            (u"Lástnäme", False, u"Fírstnäme", False),
            (u"Lástnäme", '', u"Fírstnäme", False),
            (u"Lástnäme", False, u"Fírstnäme", ''),
            (u"Lástnäme", '', u"Fírstnäme", ''),
            (u"Lástnäme", u"LástnämeSécönd", u"Fírstnäme", False),
            (u"Lástnäme", u"LástnämeSécönd", u"Fírstnäme", ''),
        )
        for l, ls, f, fn in cases:
            self.next_case()
            self.changed = self.partner_contact_create(l, ls, f)
            self.expect(l, ls, f)
            self.changed.write({'firstname': fn})
            self.expect(l, ls, fn)
        for l, ls, f, fn in cases:
            self.next_case()
            with self.env.do_in_onchange():
                # User presses ``new``
                self.changed = self.new_partner(False)
                # User sets firstname, which triggers onchanges
                self.changed.firstname = f
                self.changed._onchange_subnames()
                self.changed._onchange_name()
                self.expect(False, False, f)
                # User changes firstname, which triggers onchanges
                self.changed.firstname = fn
                self.changed._onchange_subnames()
                self.changed._onchange_name()
                self.expect(False, False, fn)

    def test_only_lastname(self):
        """Create/update a contact with only lastname."""
        cases = (
            (False, False, u"Lástnäme", u"Chängéd"),
            (False, '', u"Lástnäme", u"Chängéd"),
            ('', False, u"Lástnäme", u"Chängéd"),
            ('', '', u"Lástnäme", u"Chängéd"),
            (False, False, u"Lástnäme1 Lástnäme2", u"Chängéd1 Chängéd2"),
            (False, '', u"Lástnäme1 Lástnäme2", u"Chängéd1 Chängéd2"),
            ('', False, u"Lástnäme1 Lástnäme2", u"Chängéd1 Chängéd2"),
            ('', '', u"Lástnäme1 Lástnäme2", u"Chängéd1 Chängéd2"),
            (u"Fírstnäme", False, u"Lástnäme", False),
            (u"Fírstnäme", '', u"Lástnäme", False),
            (u"Fírstnäme", False, u"Lástnäme", ''),
            (u"Fírstnäme", '', u"Lástnäme", ''),
            (u"Fírstnäme", u"LástnämeSécönd", u"Lástnäme", False),
            (u"Fírstnäme", u"LástnämeSécönd", u"Lástnäme", ''),
        )
        for f, ls, l, ln in cases:
            self.next_case()
            self.changed = self.partner_contact_create(l, ls, f)
            self.expect(l, ls, f)
            self.changed.write({'lastname': ln})
            self.expect(ln, ls, f)
        for f, ls, l, ln in cases:
            self.next_case()
            with self.env.do_in_onchange():
                # User presses ``new``
                self.changed = self.new_partner(False)
                # User sets firstname, which triggers onchanges
                self.changed.lastname = l
                self.changed._onchange_subnames()
                self.changed._onchange_name()
                self.expect(l, False, False)
                # User changes firstname, which triggers onchanges
                self.changed.lastname = ln
                self.changed._onchange_subnames()
                self.changed._onchange_name()
                self.expect(ln, False, False)

    def test_only_lastname_second(self):
        """Create/update a contact with only lastname second."""
        cases = (
            (False, False, u"LástnämeSécönd", u"Chängéd"),
            (False, '', u"LástnämeSécönd", u"Chängéd"),
            ('', False, u"LástnämeSécönd", u"Chängéd"),
            ('', '', u"LástnämeSécönd", u"Chängéd"),
            (False, False, u"LástnämeSécönd1 Sécönd2", u"Chängéd1 Chängéd2"),
            (False, '', u"LástnämeSécönd1 Sécönd2", u"Chängéd1 Chängéd2"),
            ('', False, u"LástnämeSécönd1 Sécönd2", u"Chängéd1 Chängéd2"),
            ('', '', u"LástnämeSécönd1 Sécönd2", u"Chängéd1 Chängéd2"),
            (u"Fírstnäme", False, u"LástnämeSécönd", False),
            (u"Fírstnäme", '', u"LástnämeSécönd", False),
            (u"Fírstnäme", False, u"LástnämeSécönd", ''),
            (u"Fírstnäme", '', u"LástnämeSécönd", ''),
            (u"Fírstnäme", u"Lástnäme", u"LástnämeSécönd", False),
            (u"Fírstnäme", u"Lástnäme", u"LástnämeSécönd", ''),
        )
        for f, l, ls, lsn in cases:
            self.next_case()
            self.changed = self.partner_contact_create(l, ls, f)
            self.expect(l, ls, f)
            self.changed.write({'lastname_second': lsn})
            self.expect(l, lsn, f)
        for f, l, ls, lsn in cases:
            self.next_case()
            with self.env.do_in_onchange():
                # User presses ``new``
                self.changed = self.new_partner(False)
                # User sets firstname, which triggers onchanges
                self.changed.lastname_second = ls
                self.changed._onchange_subnames()
                self.changed._onchange_name()
                self.expect(False, ls, False)
                # User changes firstname, which triggers onchanges
                self.changed.lastname_second = lsn
                self.changed._onchange_subnames()
                self.changed._onchange_name()
                self.expect(False, lsn, False)

    def test_names(self):
        """Create/update a contact with firstnames and lastnames."""
        cases = (
            (u"Fírstnäme", u"Lástnäme", u"Sécönd",
             u"FírstnämeChängéd", u"LástnämeChängéd",
             u"SécöndChängéd"),
            (u"Fírstnäme1 Fírstnäme2", u"Lástnäme", u"Sécönd",
             u"Fírstnäme1 Fírstnäme2Chängéd", u"LástnämeChängéd",
             u"SécöndChängéd"),
            (u"Fírstnäme", u"Lástnäme1 Lástnäme2", u"Sécönd",
             u"FírstnämeChängéd", u"Lástnäme1 Lástnäme2Chängéd",
             u"SécöndChängéd"),
            (u"Fírstnäme", u"Lástnäme", u"Sécönd1 Sécönd2",
             u"FírstnämeChängéd", u"LástnämeChängéd",
             u"Sécönd1 Sécönd2Chängéd"),
            (u"Fírstnäme1 Fírstnäme2", u"Lástnäme", u"Sécönd1 Sécönd2",
             u"Fírstnäme1 Fírstnäme2Chängéd", u"LástnämeChängéd",
             u"Sécönd1 Sécönd2Chängéd"),
            (u"Fírstnäme", u"Lástnäme1 Lástnäme2", u"Sécönd1 Sécönd2",
             u"FírstnämeChängéd", u"Lástnäme1 Lástnäme2Chängéd",
             u"Sécönd1 Sécönd2Chängéd"),
            (u"Fírstnäme1 Fírstnäme2", u"Lástnäme1 Lástnäme2", u"Sécönd",
             u"Fírstnäme1 Fírstnäme2Chängéd", u"Lástnäme1 Lástnäme2Chängéd",
             u"SécöndChängéd"),
            (u"Fírstnäme1 Fírstnäme2", u"Lástnäme1 Lástnäme2", u"Sécönd1 And2",
             u"Fírstnäme1 Fírstnäme2Chängéd", u"Lástnäme1 Lástnäme2Chängéd",
             u"Sécönd1 Sécönd2Chängéd"),
        )
        for f, l, ls, fn, ln, lsn in cases:
            self.next_case()
            self.changed = self.partner_contact_create(l, ls, f)
            self.expect(l, ls, f)
            self.changed.write({
                'lastname': ln, 'lastname_second': lsn, 'firstname': fn})
            self.expect(ln, lsn, fn)
        for f, l, ls, fn, ln, lsn in cases:
            self.next_case()
            with self.env.do_in_onchange():
                # User presses ``new``
                self.changed = self.new_partner(False)
                # User sets firstname, which triggers onchanges
                self.changed.firstname = f
                self.changed._onchange_subnames()
                self.changed._onchange_name()
                # User sets lastname, which triggers onchanges
                self.changed.lastname = l
                self.changed._onchange_subnames()
                self.changed._onchange_name()
                # User sets lastname_second, which triggers onchanges
                self.changed.lastname_second = ls
                self.changed._onchange_subnames()
                self.changed._onchange_name()
                self.expect(l, ls, f)
                # User changes firstname, which triggers onchanges
                self.changed.firstname = fn
                self.changed._onchange_subnames()
                self.changed._onchange_name()
                # User changes lastname, which triggers onchanges
                self.changed.lastname = ln
                self.changed._onchange_subnames()
                self.changed._onchange_name()
                # User changes lastname_second, which triggers onchanges
                self.changed.lastname_second = lsn
                self.changed._onchange_subnames()
                self.changed._onchange_name()
                self.expect(ln, lsn, fn)

    def test_whitespaces(self):
        """Create/update a contact with names with several whitespaces."""
        cases = (
            ("  F1   F2  ", "  L1   L2   ", "  LS1   LS2   ",
             u"F1 F2", u"L1 L2", u"LS1 LS2",
             "  C1   C2  ", "  D1   D2   ", "  E1   E2   ",
             u"C1 C2", u"D1 D2", u"E1 E2"),
            ("    ", "  L1   L2   ", "  LS1   LS2   ",
             u"", u"L1 L2", u"LS1 LS2",
             "  C1   C2  ", "     ", "  E1   E2   ",
             u"C1 C2", u"", u"E1 E2"),
            ("  F1   F2  ", "     ", "  LS1   LS2   ",
             u"F1 F2", u"", u"LS1 LS2",
             "    ", "  D1   D2   ", "  E1   E2   ",
             u"", u"D1 D2", u"E1 E2"),
            ("  F1   F2  ", "  L1   L2   ", "     ",
             u"F1 F2", u"L1 L2", u"",
             "  C1   C2  ", "  D1   D2   ", "     ",
             u"C1 C2", u"D1 D2", u""),
        )
        for f, l, ls, fc, lc, lsc, fn, ln, lsn, fnc, lnc, lsnc in cases:
            self.next_case()
            self.changed = self.partner_contact_create(l, ls, f)
            self.expect(lc, lsc, fc)
            self.changed.write({
                'lastname': ln, 'lastname_second': lsn, 'firstname': fn})
            self.expect(lnc, lsnc, fnc)
        for f, l, ls, fc, lc, lsc, fn, ln, lsn, fnc, lnc, lsnc in cases:
            self.next_case()
            with self.env.do_in_onchange():
                # User presses ``new``
                self.changed = self.new_partner(False)
                # User sets firstname, which triggers onchanges
                self.changed.firstname = f
                self.changed._onchange_subnames()
                self.changed._onchange_name()
                # User sets lastname, which triggers onchanges
                self.changed.lastname = l
                self.changed._onchange_subnames()
                self.changed._onchange_name()
                # User sets lastname_second, which triggers onchanges
                self.changed.lastname_second = ls
                self.changed._onchange_subnames()
                self.changed._onchange_name()
                self.expect(lc, lsc, fc)
                # User changes firstname, which triggers onchanges
                self.changed.firstname = fn
                self.changed._onchange_subnames()
                self.changed._onchange_name()
                # User changes lastname, which triggers onchanges
                self.changed.lastname = ln
                self.changed._onchange_subnames()
                self.changed._onchange_name()
                # User changes lastname_second, which triggers onchanges
                self.changed.lastname_second = lsn
                self.changed._onchange_subnames()
                self.changed._onchange_name()
                self.expect(lnc, lsnc, fnc)

    def test_copy(self):
        """Copy a contact."""
        cases = (
            (u"Fírstnäme", u"Lástnäme", u"Sécönd",
             u"Sécönd Fírstnäme (copy)", u"Lástnäme", False),
            (u"Fírstnäme1 Fírstnäme2", u"Lástnäme", u"Sécönd",
             u"Sécönd Fírstnäme1 Fírstnäme2 (copy)", u"Lástnäme", False),
            ("", u"Lástnäme", u"Sécönd",
             u"Sécönd (copy)", u"Lástnäme", False),
            ("  ", u"Lástnäme", u"Sécönd",
             u"Sécönd (copy)", u"Lástnäme", False),
            (False, u"Lástnäme", u"Sécönd",
             u"Sécönd (copy)", u"Lástnäme", False),
            (u"Fírstnäme", u"", u"Sécönd",
             u"Fírstnäme (copy)", u"Sécönd", False),
            (u"Fírstnäme", u"  ", u"Sécönd",
             u"Fírstnäme (copy)", u"Sécönd", False),
            (u"Fírstnäme1 Fírstnäme2", "", u"Sécönd",
             u"Fírstnäme1 Fírstnäme2 (copy)", u"Sécönd", False),
            (u"Fírstnäme1 Fírstnäme2", "  ", u"Sécönd",
             u"Fírstnäme1 Fírstnäme2 (copy)", u"Sécönd", False),
            (u"Fírstnäme1 Fírstnäme2", False, u"Sécönd",
             u"Fírstnäme1 Fírstnäme2 (copy)", u"Sécönd", False),
        )
        for f, l, ls, fc, lc, lsc in cases:
            self.next_case()
            self.changed = self.partner_contact_create(l, ls, f)
            self.expect(l, ls, f)
            self.changed = self.original.with_context(lang="en_US").copy()
            self.expect(lc, lsc, fc)


class UserContactCase(PartnerContactCase):
    def partner_contact_create(self, lastname, lastname_second, firstname):
        return self.user_create(lastname, lastname_second, firstname)


class PartnerContactCaseInverse(PartnerContactCase):
    def setUp(self):
        super(PartnerContactCaseInverse, self).setUp()
        self.company.names_order = 'first_last'

    def _join_names(self, lastname, lastname_second, firstname):
        return super(PartnerContactCaseInverse, self)._join_names(
            firstname, lastname, lastname_second)

    def test_copy(self):
        """Copy a contact."""
        cases = (
            (u"Fírstnäme", u"Lástnäme", u"Sécönd",
             u"Fírstnäme", u"Lástnäme Sécönd", u"(copy)"),
            (u"Fírstnäme1 Fírstnäme2", u"Lástnäme", u"Sécönd",
             u"Fírstnäme1", u"Fírstnäme2 Lástnäme Sécönd", u"(copy)"),
            ("", u"Lástnäme", u"Sécönd",
             u"Lástnäme", u"Sécönd", u"(copy)"),
            ("  ", u"Lástnäme", u"Sécönd",
             u"Lástnäme", u"Sécönd", u"(copy)"),
            (False, u"Lástnäme", u"Sécönd",
             u"Lástnäme", u"Sécönd", u"(copy)"),
            (u"Fírstnäme", u"", u"Sécönd",
             u"Fírstnäme", u"Sécönd", u"(copy)"),
            (u"Fírstnäme", u"  ", u"Sécönd",
             u"Fírstnäme", u"Sécönd", u"(copy)"),
            (u"Fírstnäme1 Fírstnäme2", "", u"Sécönd",
             u"Fírstnäme1", u"Fírstnäme2 Sécönd", u"(copy)"),
            (u"Fírstnäme1 Fírstnäme2", "  ", u"Sécönd",
             u"Fírstnäme1", u"Fírstnäme2 Sécönd", u"(copy)"),
            (u"Fírstnäme1 Fírstnäme2", False, u"Sécönd",
             u"Fírstnäme1", u"Fírstnäme2 Sécönd", u"(copy)"),
        )
        for f, l, ls, fc, lc, lsc in cases:
            self.next_case()
            self.changed = self.partner_contact_create(l, ls, f)
            self.expect(l, ls, f)
            self.changed = self.original.with_context(lang="en_US").copy()
            self.expect(lc, lsc, fc)
