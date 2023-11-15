# Copyright 2019-2020: Druidoo (<https://www.druidoo.io>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests import common


class TestResPartner(common.TransactionCase):
    def setUp(self):
        super(TestResPartner, self).setUp()
        self.partner_admin = self.env.ref("base.partner_admin")
        self.partner_admin.write({"birthdate_date": "1991-09-05"})

    def test_compute_age(self):
        self.partner_admin._compute_age()
        age = relativedelta(
            fields.Date.today(), self.partner_admin.birthdate_date
        ).years
        self.assertEqual(self.partner_admin.age, age)
