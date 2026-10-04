# Copyright 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


class TestPartnerIdentificationNotification(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.IdCategory = cls.env["res.partner.id_category"]
        cls.IdNumber = cls.env["res.partner.id_number"]
        cls.today = fields.Date.today()

        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.email_template = cls.env["mail.template"].create(
            {
                "name": "Test Expiry Template",
                "model_id": cls.env["ir.model"]._get_id("res.partner.id_number"),
                "subject": "ID Expiring Soon",
                "body_html": "Your ID is expiring soon.",
            }
        )
        cls.id_category = cls.IdCategory.create(
            {
                "code": "test_id",
                "name": "Test ID",
                "send_notification": True,
                "days_before_expire": 5,
                "email_template_id": cls.email_template.id,
            }
        )

    def _create_id_number(self, valid_until, **vals):
        values = {
            "name": f"ID-{valid_until}",
            "partner_id": self.partner.id,
            "category_id": self.id_category.id,
            "valid_from": self.today - timedelta(days=30),
            "valid_until": valid_until,
            "status": "open",
        }
        values.update(vals)
        return self.IdNumber.create(values)

    def test_id_category_model_defaults(self):
        self.assertEqual(
            self.id_category.id_number_model_id.model, "res.partner.id_number"
        )

    def test_notify_before_expiry(self):
        """IDs expiring within the window are notified before expiry"""
        id_number = self._create_id_number(self.today + timedelta(days=3))
        self.IdNumber.send_notification()
        self.assertEqual(id_number.notification_date, self.today)

    def test_notify_on_window_bounds(self):
        """The first and last day of the window are both notified"""
        first_day = self._create_id_number(self.today + timedelta(days=5))
        last_day = self._create_id_number(self.today)
        self.IdNumber.send_notification()
        self.assertEqual(first_day.notification_date, self.today)
        self.assertEqual(last_day.notification_date, self.today)

    def test_no_notification_outside_window(self):
        """IDs expiring after the window are not notified yet"""
        id_number = self._create_id_number(self.today + timedelta(days=6))
        self.IdNumber.send_notification()
        self.assertFalse(id_number.notification_date)

    def test_no_notification_after_expiry(self):
        """Already expired IDs are not notified"""
        id_number = self._create_id_number(self.today - timedelta(days=1))
        self.IdNumber.send_notification()
        self.assertFalse(id_number.notification_date)

    def test_no_notification_without_expiry(self):
        id_number = self._create_id_number(False)
        self.IdNumber.send_notification()
        self.assertFalse(id_number.notification_date)

    def test_no_notification_when_disabled(self):
        self.id_category.send_notification = False
        id_number = self._create_id_number(self.today + timedelta(days=3))
        self.IdNumber.send_notification()
        self.assertFalse(id_number.notification_date)

    def test_no_notification_for_draft(self):
        id_number = self._create_id_number(
            self.today + timedelta(days=3), status="draft"
        )
        self.IdNumber.send_notification()
        self.assertFalse(id_number.notification_date)

    def test_no_duplicate_notification(self):
        """An already notified ID is not notified again"""
        earlier = self.today - timedelta(days=1)
        id_number = self._create_id_number(
            self.today + timedelta(days=3), notification_date=earlier
        )
        self.IdNumber.send_notification()
        self.assertEqual(id_number.notification_date, earlier)

    def test_renewal_resets_notification(self):
        """Renewing an ID (new expiry date) re-arms the notification"""
        id_number = self._create_id_number(self.today + timedelta(days=3))
        self.IdNumber.send_notification()
        self.assertEqual(id_number.notification_date, self.today)

        id_number.valid_until = self.today + timedelta(days=365)
        self.assertFalse(id_number.notification_date)

        # Renewed ID approaching its new expiry is notified again
        id_number.valid_until = self.today + timedelta(days=2)
        self.IdNumber.send_notification()
        self.assertEqual(id_number.notification_date, self.today)

    def test_explicit_notification_date_kept_on_write(self):
        id_number = self._create_id_number(self.today + timedelta(days=30))
        id_number.write(
            {
                "valid_until": self.today + timedelta(days=60),
                "notification_date": self.today,
            }
        )
        self.assertEqual(id_number.notification_date, self.today)

    def test_notification_date_not_copied(self):
        id_number = self._create_id_number(
            self.today + timedelta(days=3), notification_date=self.today
        )
        self.assertFalse(id_number.copy().notification_date)
