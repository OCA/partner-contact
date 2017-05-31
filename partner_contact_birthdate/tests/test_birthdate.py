# -*- coding: utf-8 -*-
# Copyright (C) 2014-2015  Grupo ESOC <www.grupoesoc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields
from openerp.tests.common import TransactionCase
from datetime import date


class GoodCase(TransactionCase):
    def setUp(self):
        super(GoodCase, self).setUp()
        self.partner = self.env["res.partner"].create({"name": str(self)})
        self.birthdate = date.today()

    def tearDown(self):
        self.assertEqual(self.partner.birthdate, self.partner.birthdate_date)
        super(GoodCase, self).tearDown()

    def test_new_to_old(self):
        self.partner.birthdate_date = self.birthdate

    def test_old_to_new(self):
        self.partner.birthdate = fields.Date.to_string(self.birthdate)


class BadCase(TransactionCase):
    def setUp(self):
        super(BadCase, self).setUp()
        self.partner = self.env["res.partner"].create({"name": str(self)})

    def test_old_to_new(self):
        with self.assertRaises(ValueError):
            self.partner.birthdate = "Not a date"
