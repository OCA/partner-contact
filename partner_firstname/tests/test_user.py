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


#class UserCase(BaseCase):
#    def test_create_false_names(self):
#        """Create an user with False name."""
#        self.check_fields = False
#        with self.assertRaises(ex.EmptyNamesError):
#            self.user_create(False, False, False)
#
#    def test_create_no_name(self):
#        """Create an user with empty name."""
#        self.check_fields = False
#        with self.assertRaises(ex.EmptyNamesError):
#            self.user_create(False, False, '')
#
#    def test_create_one_name(self):
#        """Create an user with one name."""
#        name = u"Näme"
#        self.user_create(False, False, name)
#        self.expect(name, False, name)
