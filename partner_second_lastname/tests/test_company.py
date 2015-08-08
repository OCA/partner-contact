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


class PartnerCompanyCase(BaseCase):
    def test_empty_name(self):
        """Create/update a company with False/empty name."""
        name = u"Näme1 Näme2"
        cases = (
            False,
            '',
            '   ',
        )
        with self.assertRaises(ex.EmptyNamesError):
            for n in cases:
                self.next_case()
                self.partner_company_create(n)
        self.changed = self.partner_company_create(name)
        with self.assertRaises(ex.EmptyNamesError):
            for n in cases:
                self.next_case()
                self.changed.write({'name': n})
        for n in cases:
            self.next_case()
            with self.env.do_in_onchange():
                # User presses ``new``
                self.changed = self.new_partner(True)
                # User sets a name, which triggers onchanges
                self.changed.name = n
                self.changed._onchange_name()
                self.expect(False, False, False)
        for n in cases:
            self.next_case()
            with self.env.do_in_onchange():
                # User presses ``new``
                self.changed = self.new_partner(True)
                # User sets a name, which triggers onchanges
                self.changed.name = name
                self.changed._onchange_name()
                self.expect(name, False, False)
                # User unsets name, which triggers onchanges
                self.changed.name = n
                self.changed._onchange_name()
                self.expect(False, False, False)

    def test_name(self):
        """Create a company with name."""
        cases = (
            (u"Näme", u"Chängéd"),
            (u"Näme1 Näme2", u"Chängéd1 Chängéd2"),
            (u"Näme1 Näme2 Näme3", u"Chängéd1 Chängéd2 Chängéd3"),
            (u"Näme1 Näme2 Näme3", u"Chängéd1 Chängéd2"),
            (u"Näme1 Näme2 Näme3", u"Chängéd"),
        )
        for n, nn in cases:
            self.next_case()
            self.changed = self.partner_company_create(n)
            self.expect(n, False, False, n)
            self.changed.write({'name': nn})
            self.expect(nn, False, False, nn)
        for n, nn in cases:
            self.next_case()
            with self.env.do_in_onchange():
                # User presses ``new``
                self.changed = self.new_partner(True)
                # User sets a name, which triggers onchanges
                self.changed.name = n
                self.changed._onchange_name()
                self.expect(n, False, False)
                # User unsets name, which triggers onchanges
                self.changed.name = nn
                self.changed._onchange_name()
                self.expect(nn, False, False)

    def test_whitespaces(self):
        """Create/update a company with name with several whitespaces."""
        cases = (
            (u"   Näme  ", u"Näme",
             u"  Chängéd   ", u"Chängéd"),
            (u"  Näme1   Näme2   ", u"Näme1 Näme2",
             u"   Chängéd1     Chängéd2  ", u"Chängéd1 Chängéd2"),
            (u"  N1  N2    N3   ", u"N1 N2 N3",
             u"   C1   C2  C3  ", u"C1 C2 C3"),
        )
        for n, nc, nn, nnc in cases:
            self.next_case()
            self.changed = self.partner_company_create(n)
            self.expect(nc, False, False, nc)
            self.changed.write({'name': nn})
            self.expect(nnc, False, False, nnc)
        for n, nc, nn, nnc in cases:
            self.next_case()
            with self.env.do_in_onchange():
                # User presses ``new``
                self.changed = self.new_partner(True)
                # User sets a name, which triggers onchanges
                self.changed.name = n
                self.changed._onchange_name()
                self.expect(nc, False, False)
                # User unsets name, which triggers onchanges
                self.changed.name = nn
                self.changed._onchange_name()
                self.expect(nnc, False, False)

    def test_copy(self):
        """Copy a company."""
        cases = (
            (u"Näme", u"Näme (copy)"),
            (u"Näme1 Näme2", u"Näme1 Näme2 (copy)"),
            (u"Näme1 Näme2 Näme3", u"Näme1 Näme2 Näme3 (copy)"),
        )
        for n, nc in cases:
            self.next_case()
            self.changed = self.partner_company_create(n)
            self.expect(n, False, False, n)
            self.changed = self.original.with_context(lang="en_US").copy()
            self.expect(nc, False, False, nc)


class PartnerCompanyCaseInverse(PartnerCompanyCase):
    def setUp(self):
        super(PartnerCompanyCaseInverse, self).setUp()
        self.company.names_order = 'first_last'
