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
    pass


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
