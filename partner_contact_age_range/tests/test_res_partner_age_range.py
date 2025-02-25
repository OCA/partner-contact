# Copyright 2019-2020: Druidoo (<https://www.druidoo.io>)
# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime

from dateutil.relativedelta import relativedelta
from freezegun import freeze_time

from odoo.exceptions import ValidationError

from odoo.addons.base.tests.common import BaseCommon


class TestRespartnerAgeRange(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.range_model = cls.env["res.partner.age.range"]
        cls.partner_model = cls.env["res.partner"]
        cls.baby_range = cls.range_model.create(
            {"name": "baby", "age_from": 0, "age_to": 2}
        )
        cls.partner = cls.partner_model.create(
            {
                "name": "Test",
                "birthdate_date": datetime.today() - relativedelta(years=1, days=10),
            }
        )
        cls.partner2 = cls.partner_model.create(
            {
                "name": "Test2",
                "birthdate_date": datetime.today() + relativedelta(years=1),
            }
        )

    @freeze_time("2024-02-07")
    def test_age_from(self):
        age_from = self.range_model._default_age_from()
        toddler_range = self.range_model.create(
            {"name": "Toddler", "age_from": age_from, "age_to": 4}
        )
        self.assertEqual(toddler_range.age_from, self.baby_range.age_to + 1)

    @freeze_time("2024-02-07")
    def test_validate_range(self):
        with self.assertRaises(ValidationError):
            self.range_model.create({"name": "Child", "age_from": 1, "age_to": 12})
        with self.assertRaises(ValidationError):
            self.range_model.create({"name": "Teenager", "age_from": 16, "age_to": 15})

    @freeze_time("2024-02-07")
    def test_cron_update_age_range_id(self):
        self.partner_model._cron_update_age_range_id()
        self.assertEqual(self.partner.age_range_id, self.baby_range)

    @freeze_time("2024-02-07")
    def test_partner_norange(self):
        self.assertFalse(self.partner2.age_range_id)
