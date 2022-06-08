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

        self.partner_demo = self.env.ref("base.partner_demo")
        self.partner_demo.write({"birthdate_date": "2100-01-01"})

    def test_compute_age(self):
        self.partner_admin._compute_age()
        age = relativedelta(
            fields.Date.today(), self.partner_admin.birthdate_date
        ).years
        self.assertEqual(self.partner_admin.age, age)

    def test_search_age_unexpected_operator(self):
        self.partner_admin._compute_age()
        self.assertEqual(self.partner_admin._search_age("like", "0"), [])

    def test_search_age_correct_result(self):
        self.partner_admin._compute_age()
        self.assertEqual(
            self.partner_admin._search_age(">=", "1"),
            [("id", "in", [self.env.ref("base.partner_admin").id])],
        )

    def test_search_age_same_as_compute_age(self):
        self.partner_admin._compute_age()
        self.assertEqual(
            self.partner_admin._search_age("=", self.partner_admin.age),
            [("id", "in", [self.env.ref("base.partner_admin").id])],
        )

    def test_search_age_same_as_compute_age_for_negative_age(self):
        self.partner_admin._compute_age()
        self.partner_demo._compute_age()
        self.assertEqual(
            self.partner_demo._search_age("=", self.partner_demo.age),
            [("id", "in", [self.env.ref("base.partner_demo").id])],
        )
