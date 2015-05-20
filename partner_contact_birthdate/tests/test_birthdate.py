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

from openerp import fields
from openerp.tests.common import TransactionCase
from datetime import date


class BirthdateCase(TransactionCase):
    def setUp(self):
        super(BirthdateCase, self).setUp()
        self.partner = self.env["res.partner"].create({"name": str(self)})
        self.birthdate = date.today()

    def tearDown(self):
        self.assertEqual(self.partner.birthdate, self.partner.birthdate_date)
        super(BirthdateCase, self).tearDown()

    def test_new_to_old(self):
        self.partner.birthdate_date = self.birthdate

    def test_old_to_new(self):
        self.partner.birthdate = fields.Date.to_string(self.birthdate)
