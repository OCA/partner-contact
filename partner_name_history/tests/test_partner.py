#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime

from dateutil.relativedelta import relativedelta

from odoo.tests import Form, TransactionCase

from .common import _get_name_from_date, _set_partner_name


class TestPartner(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        partner_form = Form(cls.env["res.partner"])
        partner_form.name = "Test"
        cls.partner = partner_form.save()

    def test_context_partner_name_date(self):
        """Context key `partner_name_date` allows to return
        the name according to the partner's history."""
        # Arrange
        partner = self.partner
        original_partner_name = partner.name
        change_datetimes = [
            datetime.datetime(2019, 1, 1),
            datetime.datetime(2020, 1, 1),
        ]

        # Act
        datetime_to_names = {
            date: _get_name_from_date(date) for date in change_datetimes
        }
        for test_datetime, name in datetime_to_names.items():
            _set_partner_name(
                partner,
                name,
                date=test_datetime,
            )

        # Assert
        one_day = relativedelta(days=1)
        datetime_to_expected_name = {
            change_datetimes[0] - one_day: original_partner_name,
            change_datetimes[0] + one_day: _get_name_from_date(change_datetimes[0]),
            change_datetimes[1] - one_day: _get_name_from_date(change_datetimes[0]),
            change_datetimes[1] + one_day: partner.name,
        }
        for test_datetime, expected_name in datetime_to_expected_name.items():
            # Otherwise the same value is returned everytime
            # because it is in cache
            partner.invalidate_recordset(
                fnames=[
                    "name",
                ],
            )
            self.assertEqual(
                expected_name,
                partner.with_context(partner_name_date=test_datetime).name,
            )
