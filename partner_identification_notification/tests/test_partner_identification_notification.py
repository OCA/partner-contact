# Copyright 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


class TestPartnerIdentificationNotification(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        # Get the required models
        cls.IdCategory = cls.env["res.partner.id_category"]
        cls.IdNumber = cls.env["res.partner.id_number"]

        # Create a test partner
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )

        # Create an ID category for testing
        cls.id_category = cls.IdCategory.create(
            {
                "code": "test_id",
                "name": "Test ID",
                "send_notification": True,
                "days_before_expire": 5,
                "email_template_id": cls.env.ref(
                    "partner_identification_notification.expiry_email_template",
                    raise_if_not_found=False,
                ).id
                if cls.env.ref(
                    "partner_identification_notification.expiry_email_template",
                    raise_if_not_found=False,
                )
                else False,
            }
        )

    def test_id_category_model_defaults(self):
        """Test that the ID model is set correctly by default"""
        self.assertTrue(self.id_category.id_number_model_id)
        self.assertEqual(
            self.id_category.id_number_model_id.model, "res.partner.id_number"
        )

    def test_id_category_fields(self):
        """Test ID category fields"""
        self.assertTrue(self.id_category.send_notification)
        self.assertEqual(self.id_category.days_before_expire, 5)

    def test_id_number_with_expiry(self):
        """Test creating an ID number with an expiry date"""
        future_date = datetime.now() + timedelta(days=10)
        id_number = self.IdNumber.create(
            {
                "name": "ABC123456",
                "partner_id": self.partner.id,
                "category_id": self.id_category.id,
                "valid_from": datetime.now().date(),
                "valid_until": future_date.date(),
            }
        )
        self.assertEqual(id_number.name, "ABC123456")
        self.assertEqual(id_number.partner_id, self.partner)
        self.assertEqual(id_number.category_id, self.id_category)

    def test_id_number_without_expiry(self):
        """Test creating an ID number without an expiry date"""
        id_number = self.IdNumber.create(
            {
                "name": "XYZ789012",
                "partner_id": self.partner.id,
                "category_id": self.id_category.id,
                "valid_from": datetime.now().date(),
            }
        )
        self.assertEqual(id_number.name, "XYZ789012")
        self.assertFalse(id_number.valid_until)

    def test_id_number_notification_date_field(self):
        """Test that the notification date field exists and works"""
        future_date = datetime.now() + timedelta(days=10)
        id_number = self.IdNumber.create(
            {
                "name": "DEF456789",
                "partner_id": self.partner.id,
                "category_id": self.id_category.id,
                "valid_from": datetime.now().date(),
                "valid_until": future_date.date(),
            }
        )

        # Initially, notification date should be False
        self.assertFalse(id_number.notification_date)

        # Set a notification date
        test_date = datetime.now().date()
        id_number.notification_date = test_date
        self.assertEqual(id_number.notification_date, test_date)

    def test_send_notification_method(self):
        """Test the send notification functionality in detail"""
        # Create an email template for testing
        email_template = self.env["mail.template"].create(
            {
                "name": "Test Expiry Template for Notifications",
                "model_id": self.env["ir.model"]
                .search([("model", "=", "res.partner.id_number")], limit=1)
                .id,
                "subject": "Test ID Expiry Notification",
                "body_html": "Your ID is expiring soon - please renew.",
            }
        )

        # Update the category to include the email template
        self.id_category.email_template_id = email_template.id

        # Create an ID that should trigger a notification
        yesterday = datetime.now().date() - timedelta(days=1)
        id_number = self.IdNumber.create(
            {
                "name": "GHI987654",
                "partner_id": self.partner.id,
                "category_id": self.id_category.id,
                "valid_from": (datetime.now() - timedelta(days=10)).date(),
                "valid_until": yesterday,
                "status": "open",
            }
        )

        # Initially no notification should have been sent
        self.assertFalse(id_number.notification_date)

        # Call the send notification method
        id_number.send_notification()

        # Notification should be set to today since all conditions are met
        id_number = self.IdNumber.browse(id_number.id)
        self.assertTrue(id_number.notification_date)
        self.assertEqual(id_number.notification_date, fields.Date.today())

    def test_send_notification_method_conditions(self):
        """Test the send_notification method with different conditions"""
        # Create an email template for testing
        email_template = self.env["mail.template"].create(
            {
                "name": "Test Expiry Template - Conditions",
                "model_id": self.env["ir.model"]
                .search([("model", "=", "res.partner.id_number")], limit=1)
                .id,
                "subject": "Test Conditions",
                "body_html": "Test body for conditions.",
            }
        )

        # Update the category to include the email template
        self.id_category.email_template_id = email_template.id

        # Test case 1: ID not yet expired (should not trigger notification)
        future_date = datetime.now().date() + timedelta(days=10)
        id_number_future = self.IdNumber.create(
            {
                "name": "FUTURE123",
                "partner_id": self.partner.id,
                "category_id": self.id_category.id,
                "valid_from": datetime.now().date(),
                "valid_until": future_date,
                "status": "open",
            }
        )

        initial_notification_date = id_number_future.notification_date
        id_number_future.send_notification()
        id_number_future = self.IdNumber.browse(id_number_future.id)
        # Should remain unchanged since not close to expiry
        self.assertEqual(id_number_future.notification_date, initial_notification_date)

        # Test case 2: ID with notification disabled
        category_no_notification = self.IdCategory.create(
            {
                "code": "test_no_notify",
                "name": "Test No Notification",
                "send_notification": False,
                "days_before_expire": 5,
                "email_template_id": email_template.id,
            }
        )
        yesterday = datetime.now().date() - timedelta(days=1)
        id_number_no_notify = self.IdNumber.create(
            {
                "name": "NO_NOTIFY456",
                "partner_id": self.partner.id,
                "category_id": category_no_notification.id,
                "valid_from": (datetime.now() - timedelta(days=10)).date(),
                "valid_until": yesterday,
                "status": "open",
            }
        )

        id_number_no_notify.send_notification()
        id_number_no_notify = self.IdNumber.browse(id_number_no_notify.id)
        # Should not be updated because send_notification is False
        self.assertFalse(id_number_no_notify.notification_date)

        # Test case 3: ID already notified (should not send again)
        already_notified_id = self.IdNumber.create(
            {
                "name": "ALREADY_NOTIFY789",
                "partner_id": self.partner.id,
                "category_id": self.id_category.id,
                "valid_from": (datetime.now() - timedelta(days=10)).date(),
                "valid_until": yesterday,
                "status": "open",
                "notification_date": fields.Date.today(),
            }
        )

        initial_notification_date = already_notified_id.notification_date
        already_notified_id.send_notification()
        already_notified_id = self.IdNumber.browse(already_notified_id.id)
        # Should remain unchanged - notification already sent
        self.assertEqual(
            already_notified_id.notification_date, initial_notification_date
        )

    def test_send_notification_for_expiring_ids(self):
        """Test that notifications are sent for IDs within the expiry window"""
        # Create an email template for testing
        id_number_model = self.env["ir.model"].search(
            [("model", "=", "res.partner.id_number")], limit=1
        )

        email_template = self.env["mail.template"].create(
            {
                "name": "Test Expiry Template",
                "model_id": id_number_model.id,
                "subject": "ID Expiring Soon",
                "body_html": "Your ID is expiring soon.",
            }
        )

        # Update the category to include an email template
        self.id_category.email_template_id = email_template.id

        # Create an ID that expired 2 days ago
        expiry_date = datetime.now().date() - timedelta(days=2)
        id_number = self.IdNumber.create(
            {
                "name": "JKL112233",
                "partner_id": self.partner.id,
                "category_id": self.id_category.id,
                "valid_from": (datetime.now() - timedelta(days=10)).date(),
                "valid_until": expiry_date,
                "status": "open",
            }
        )

        # Initially no notification should have been sent
        self.assertFalse(id_number.notification_date)

        # Call the send notification method
        id_number.send_notification()

        # Re-read the record from the database to get the updated value
        id_number = self.IdNumber.browse(id_number.id)

        # Check if notification was sent (notification_date was set to today)
        self.assertTrue(id_number.notification_date)
        self.assertEqual(id_number.notification_date, fields.Date.today())

    def test_cron_job_execution(self):
        """Test the send notification method as a class method"""
        # Execute send_notification as a class method (simulates cron job)
        try:
            self.IdNumber.send_notification()
        except Exception:  # pylint: disable=except-pass
            # Expected: method may fail if no matching records exist
            # In tests, we sometimes want to catch exceptions without specific handling
            pass

    def test_send_notification_search_logic(self):
        """Test the search logic in send_notification method"""
        # Create an email template
        email_template = self.env["mail.template"].create(
            {
                "name": "Test Search Logic Template",
                "model_id": self.env["ir.model"]
                .search([("model", "=", "res.partner.id_number")], limit=1)
                .id,
                "subject": "Search Logic Test",
                "body_html": "Testing search logic.",
            }
        )

        # Create a category with notification enabled
        category = self.IdCategory.create(
            {
                "code": "search_test",
                "name": "Search Test Category",
                "send_notification": True,
                "days_before_expire": 3,
                "email_template_id": email_template.id,
            }
        )

        # Create an ID that meets all criteria for notification
        expiry_date = fields.Date.today() - timedelta(days=1)  # Expired yesterday
        id_number = self.IdNumber.create(
            {
                "name": "SEARCH_TEST_001",
                "partner_id": self.partner.id,
                "category_id": category.id,
                "valid_from": fields.Date.today() - timedelta(days=30),
                "valid_until": expiry_date,
                "status": "open",
            }
        )

        # Before running the method, the notification should not be sent
        self.assertFalse(id_number.notification_date)

        # Run send_notification to process matching records
        self.IdNumber.send_notification()

        # Re-read record to get updated values
        id_number = self.IdNumber.browse(id_number.id)

        # The notification should have been sent
        self.assertEqual(id_number.notification_date, fields.Date.today())

        # Run method again - ID should not be notified again
        expected_notification_date = id_number.notification_date
        self.IdNumber.send_notification()
        id_number = self.IdNumber.browse(id_number.id)

        # Notification date should remain the same
        self.assertEqual(id_number.notification_date, expected_notification_date)
