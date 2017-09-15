# -*- coding: utf-8 -*-
# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from mock import patch
from datetime import datetime, timedelta
from openerp.tests.common import TransactionCase

PATH = ("openerp.addons.partner_phonecall_schedule.models"
        ".res_partner.datetime")


class CanICallCase(TransactionCase):
    def setUp(self):
        super(CanICallCase, self).setUp()
        self.some_mornings = self.env["resource.calendar"].create({
            "name": "Some mornings",
            "attendance_ids": [
                (0, 0, {
                    "name": "Friday morning",
                    "dayofweek": "4",
                    "hour_from": 8,
                    "hour_to": 12,
                }),
                (0, 0, {
                    "name": "Next monday morning",
                    "dayofweek": "0",
                    "hour_from": 8,
                    "hour_to": 12,
                    "date_from": "2017-09-18",
                    "date_to": "2017-09-18",
                }),
            ],
        })
        self.Partner = self.env["res.partner"]
        self.dude = self.Partner.create({
            "name": "Dude",
        })
        self.dude.phonecall_calendar_ids = self.some_mornings
        # This is a friday morning
        self.datetime = datetime(2017, 9, 15, 10, 53, 30)

    @patch(PATH)
    def tearDown(self, mocked_dt):
        mocked_dt.now.return_value = self.datetime
        mocked_dt.date.return_value = self.datetime.date()
        if self.allowed:
            self.assertTrue(self.dude.phonecall_available)
            self.assertTrue(self.Partner.search([
                ("id", "=", self.dude.id),
                ("phonecall_available", "=", True),
            ]))
            self.assertTrue(self.Partner.search([
                ("id", "=", self.dude.id),
                ("phonecall_available", "!=", False),
            ]))
            self.assertFalse(self.Partner.search([
                ("id", "=", self.dude.id),
                ("phonecall_available", "=", False),
            ]))
            self.assertFalse(self.Partner.search([
                ("id", "=", self.dude.id),
                ("phonecall_available", "!=", True),
            ]))
        else:
            self.assertFalse(self.dude.phonecall_available)
            self.assertFalse(self.Partner.search([
                ("id", "=", self.dude.id),
                ("phonecall_available", "=", True),
            ]))
            self.assertFalse(self.Partner.search([
                ("id", "=", self.dude.id),
                ("phonecall_available", "!=", False),
            ]))
            self.assertTrue(self.Partner.search([
                ("id", "=", self.dude.id),
                ("phonecall_available", "=", False),
            ]))
            self.assertTrue(self.Partner.search([
                ("id", "=", self.dude.id),
                ("phonecall_available", "!=", True),
            ]))
        return super(CanICallCase, self).tearDown()

    def test_friday_morning(self):
        """I can call dude this morning"""
        self.allowed = True

    def test_friday_evening(self):
        """I cannot call dude this evening"""
        self.datetime += timedelta(hours=4)
        self.allowed = False

    def test_saturday_morning(self):
        """I cannot call dude tomorrow morning"""
        self.datetime += timedelta(days=1)
        self.allowed = False

    def test_saturday_evening(self):
        """I cannot call dude tomorrow evening"""
        self.datetime += timedelta(days=1, hours=4)
        self.allowed = False

    def test_next_monday_morning(self):
        """I can call dude next monday morning"""
        self.datetime += timedelta(days=3)
        self.allowed = True

    def test_second_next_monday_morning(self):
        """I cannot call dude second next monday morning"""
        self.datetime += timedelta(days=10, hours=4)
        self.allowed = False
