# Copyright 2017 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from mock import patch

from odoo import fields
from odoo.tests.common import SavepointCase

PATH = "odoo.addons.partner_phonecall_schedule.models.res_partner.datetime"


class CanICallCase(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Calendar = cls.env["resource.calendar"].with_context(tz="UTC")
        cls.Partner = cls.env["res.partner"].with_context(tz="UTC")
        cls.some_mornings = cls.Calendar.create(
            {
                "name": "Some mornings",
                "attendance_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Friday morning",
                            "dayofweek": "4",
                            "hour_from": 8,
                            "hour_to": 12,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "Next monday morning",
                            "dayofweek": "0",
                            "hour_from": 8,
                            "hour_to": 12,
                            "date_from": "2017-09-18",
                            "date_to": "2017-09-18",
                        },
                    ),
                ],
            }
        )
        cls.some_evenings = cls.Calendar.create(
            {
                "name": "Some evenings",
                "attendance_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Friday evening",
                            "dayofweek": "4",
                            "hour_from": 15,
                            "hour_to": 19,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "Next monday evening",
                            "dayofweek": "0",
                            "hour_from": 15,
                            "hour_to": 19,
                            "date_from": "2017-09-18",
                            "date_to": "2017-09-18",
                        },
                    ),
                ],
            }
        )
        cls.dude = cls.Partner.create({"name": "Dude"})
        cls.dude.phonecall_calendar_ids = cls.some_mornings

    def setUp(self):
        super().setUp()
        # Now it is a friday morning
        self.datetime = datetime(2017, 9, 15, 10, 53, 30)

    def _allowed(self, now=None):
        dude, Partner = self.dude, self.Partner
        if now:
            dude = dude.with_context(now=now)
            Partner = Partner.with_context(now=now)
        self.assertTrue(dude.phonecall_available)
        self.assertTrue(
            Partner.search([("id", "=", dude.id), ("phonecall_available", "=", True)])
        )
        self.assertTrue(
            Partner.search([("id", "=", dude.id), ("phonecall_available", "!=", False)])
        )
        self.assertFalse(
            Partner.search([("id", "=", dude.id), ("phonecall_available", "=", False)])
        )
        self.assertFalse(
            Partner.search([("id", "=", dude.id), ("phonecall_available", "!=", True)])
        )

    def allowed(self):
        # Test mocking datetime.now()
        with patch(PATH) as mocked_dt:
            mocked_dt.now.return_value = self.datetime
            mocked_dt.date.return_value = self.datetime.date()
            self._allowed()
        # Test sending a datetime object in the context
        self._allowed(self.datetime)
        # Test sending a string in the context
        self._allowed(fields.Datetime.to_string(self.datetime))

    def _disallowed(self, now=None):
        dude, Partner = self.dude, self.Partner
        if now:
            dude = dude.with_context(now=now)
            Partner = Partner.with_context(now=now)
        self.assertFalse(dude.phonecall_available)
        self.assertFalse(
            Partner.search([("id", "=", dude.id), ("phonecall_available", "=", True)])
        )
        self.assertFalse(
            Partner.search([("id", "=", dude.id), ("phonecall_available", "!=", False)])
        )
        self.assertTrue(
            Partner.search([("id", "=", dude.id), ("phonecall_available", "=", False)])
        )
        self.assertTrue(
            Partner.search([("id", "=", dude.id), ("phonecall_available", "!=", True)])
        )

    def disallowed(self):
        # Test mocking datetime.now()
        with patch(PATH) as mocked_dt:
            mocked_dt.now.return_value = self.datetime
            mocked_dt.date.return_value = self.datetime.date()
            self._disallowed()
        # Test sending a datetime object in the context
        self._disallowed(self.datetime)
        # Test sending a string in the context
        self._disallowed(fields.Datetime.to_string(self.datetime))

    def test_friday_morning(self):
        """I can call dude this morning"""
        self.allowed()

    def test_friday_evening(self):
        """I cannot call dude this evening"""
        self.datetime += timedelta(hours=4)
        self.disallowed()

    def test_saturday_morning(self):
        """I cannot call dude tomorrow morning"""
        self.datetime += timedelta(days=1)
        self.disallowed()

    def test_saturday_evening(self):
        """I cannot call dude tomorrow evening"""
        self.datetime += timedelta(days=1, hours=4)
        self.disallowed()

    def test_next_monday_morning(self):
        """I can call dude next monday morning"""
        self.datetime += timedelta(days=3)
        self.allowed()

    def test_second_next_monday_morning(self):
        """I cannot call dude second next monday morning"""
        self.datetime += timedelta(days=10, hours=4)
        self.disallowed()

    def test_aggregated_attendances(self):
        """I get aggregated schedules correctly."""
        self.dude.phonecall_calendar_ids |= self.some_evenings
        all_attendances = (self.some_mornings | self.some_evenings).mapped(
            "attendance_ids"
        )
        self.assertEqual(self.dude.phonecall_calendar_attendance_ids, all_attendances)
