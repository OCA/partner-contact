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


class PartnerCompanyCase(BaseCase):
    def test_empty_name(self):
        """Create/update a company with False/empty name."""
        with self.assertRaises(ex.EmptyNamesError):
            self.partner_company_create(False)
            self.partner_company_create('')
            self.partner_company_create('   ')
        self.changed = self.partner_company_create(u"Näme1 Näme2")
        with self.assertRaises(ex.EmptyNamesError):
            self.changed.write({'name': False})
            self.changed.write({'name': ''})
            self.changed.write({'name': '   '})

    def test_name(self):
        """Create a company with name."""
        cases = (
            (u"Näme", u"Chängéd"),
            (u"Näme1 Näme2", u"Chängéd1 Chängéd2"),
            (u"Näme1 Näme2 Näme3", u"Chängéd1 Chängéd2 Chängéd3"),
            (u"Näme1 Näme2 Näme3", u"Chängéd1 Chängéd2"),
            (u"Näme1 Näme2 Näme3", u"Chängéd"),
        )
        for name, name_new in cases:
            self.changed = self.partner_company_create(name)
            self.expect(name, False, name)
            self.changed.write({'name': name_new})
            self.expect(name_new, False, name_new)

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
            self.changed = self.partner_company_create(n)
            self.expect(nc, False, nc)
            self.changed.write({'name': nn})
            self.expect(nnc, False, nnc)

    def test_copy(self):
        """Copy a company."""
        cases = (
            (u"Näme", u"Näme (copy)"),
            (u"Näme1 Näme2", u"Näme1 Näme2 (copy)"),
            (u"Näme1 Näme2 Näme3", u"Näme1 Näme2 Näme3 (copy)"),
        )
        for n, nc in cases:
            self.partner_company_create(n)
            self.expect(n, False, n)
            self.changed = self.original.with_context(lang="en_US").copy()
            self.expect(nc, False, nc)


class PartnerCompanyCaseInverse(PartnerCompanyCase):
    def partner_company_create(self, name):
        super(PartnerCompanyCaseInverse, self).partner_company_create(name)
        self.original.company_id.names_order = 'first_last'
