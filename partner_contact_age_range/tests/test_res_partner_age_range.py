# Copyright 2019-2020: Druidoo (<https://www.druidoo.io>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestRespartnerAgeRange(TransactionCase):
    def test_overlap(self):
        self.env["res.partner.age.range"].create(
            {"name": "baby", "age_from": 0, "age_to": 2}
        )
        with self.assertRaises(ValidationError):
            self.env["res.partner.age.range"].create(
                {"name": "Toddler", "age_from": 1, "age_to": 4}
            )
