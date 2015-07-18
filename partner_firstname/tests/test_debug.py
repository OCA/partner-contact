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
