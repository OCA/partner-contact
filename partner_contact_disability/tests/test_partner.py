# -*- coding: utf-8 -*-

# Odoo, Open Source Management Solution
# Copyright (C) 2014-2015  Grupo ESOC <www.grupoesoc.es>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from openerp.tests.common import TransactionCase
from .. import exceptions as ex


class PartnerCase(TransactionCase):
    def setUp(self):
        super(PartnerCase, self).setUp()
        self.partner = self.env["res.partner"].create({
            "name": str(self),
            "is_company": False})

    def test_good(self):
        self.partner.disability_percentage = 0
        self.partner.disability_percentage = 33
        self.partner.disability_percentage = 100

    def test_less_than_0(self):
        with self.assertRaises(ex.OutOfRangeError):
            self.partner.disability_percentage = -1

    def test_more_than_100(self):
        with self.assertRaises(ex.OutOfRangeError):
            self.partner.disability_percentage = 101
