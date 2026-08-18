import odoo
from odoo import fields
from odoo.tests import common


@odoo.tests.tagged("post_install", "-at_install")
class TestPartnerIdentificationKYC(common.TransactionCase):
    def setUp(self):
        super().setUp()

        # Get the KYC category
        self.kyc_category = self.env.ref(
            "partner_identification_kyc.kyc_identification_category"
        )

        # Create a test partner
        self.test_partner = self.env["res.partner"].create(
            {
                "name": "Test Partner for KYC",
                "email": "test.kyc@example.com",
            }
        )

        # Create a test issuer
        self.test_issuer = self.env["res.partner"].create(
            {
                "name": "Test KYC Issuer",
                "is_company": True,
            }
        )

    def test_kyc_category_creation(self):
        """Test that the KYC category was created with correct settings."""
        self.assertEqual(self.kyc_category.name, "KYC")
        self.assertEqual(self.kyc_category.code, "KYC")
        self.assertTrue(self.kyc_category.create_activity_on_new)
        self.assertEqual(self.kyc_category.default_validity_number, 1)
        self.assertEqual(self.kyc_category.default_validity_unit, "years")
        self.assertEqual(self.kyc_category.renewal_lead_number, 2)
        self.assertEqual(self.kyc_category.renewal_lead_unit, "months")

        # Check that activity types are set correctly
        activity_type = self.env.ref(
            "partner_identification_kyc.activity_type_kyc_check"
        )
        self.assertEqual(self.kyc_category.initial_activity_type_id, activity_type)
        self.assertEqual(self.kyc_category.renew_activity_type_id, activity_type)

    def test_action_request_kyc_creates_record(self):
        """Test that the action_request_kyc creates a new KYC identification record."""
        initial_count = self.env["res.partner.id_number"].search_count(
            [
                ("partner_id", "=", self.test_partner.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        )

        # Call the action
        self.test_partner.action_request_kyc()

        # Check that a new record was created
        final_count = self.env["res.partner.id_number"].search_count(
            [
                ("partner_id", "=", self.test_partner.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        )

        self.assertEqual(final_count, initial_count + 1)

        # Get the newly created record
        new_record = self.env["res.partner.id_number"].search(
            [
                ("partner_id", "=", self.test_partner.id),
                ("category_id", "=", self.kyc_category.id),
            ],
            order="create_date desc",
            limit=1,
        )

        self.assertEqual(new_record.status, "draft")
        # The ID Number is auto-assigned from the KYC sequence (prefix "KYC").
        self.assertTrue(new_record.name)
        self.assertTrue(new_record.name.startswith("KYC"))

    def test_manual_id_number_gets_sequence(self):
        """A KYC ID record created manually (no name) gets the sequence."""
        record = self.env["res.partner.id_number"].create(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.kyc_category.id,
            }
        )
        self.assertTrue(record.name)
        self.assertTrue(record.name.startswith("KYC"))

    def test_onchange_category_prefills_name(self):
        """Selecting the KYC category prefills the (required) ID Number."""
        record = self.env["res.partner.id_number"].new(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.kyc_category.id,
            }
        )
        self.assertFalse(record.name)
        record._onchange_category_id_kyc_name()
        # The required ID Number is filled automatically, so the record is savable.
        self.assertTrue(record.name)
        self.assertTrue(record.name.startswith("KYC"))

    def test_manual_id_number_keeps_provided_name(self):
        """An explicit ID Number is not overwritten by the sequence."""
        record = self.env["res.partner.id_number"].create(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.kyc_category.id,
                "name": "MY-CUSTOM-ID",
            }
        )
        self.assertEqual(record.name, "MY-CUSTOM-ID")

    def test_action_request_kyc_duplicate_prevention(self):
        """Test that action_request_kyc prevents duplicates when a 'draft' record
        already exists."""
        # Create the first KYC record
        self.test_partner.action_request_kyc()

        # Verify the first record exists
        records = self.env["res.partner.id_number"].search(
            [
                ("partner_id", "=", self.test_partner.id),
                ("category_id", "=", self.kyc_category.id),
                ("status", "=", "draft"),
            ]
        )
        self.assertEqual(len(records), 1)

        # Try to create another record - should raise an error
        with self.assertRaises(odoo.exceptions.UserError):
            self.test_partner.action_request_kyc()

    def test_ensure_kyc_record_creates_when_none_exists(self):
        """Test that ensure_kyc_record creates a record when none exists."""
        initial_count = self.env["res.partner.id_number"].search_count(
            [
                ("partner_id", "=", self.test_partner.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        )

        # Call the API function
        self.test_partner.ensure_kyc_record()

        # Check that a new record was created
        final_count = self.env["res.partner.id_number"].search_count(
            [
                ("partner_id", "=", self.test_partner.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        )

        self.assertEqual(final_count, initial_count + 1)

        # Verify the status is 'draft'
        new_record = self.env["res.partner.id_number"].search(
            [
                ("partner_id", "=", self.test_partner.id),
                ("category_id", "=", self.kyc_category.id),
            ],
            order="create_date desc",
            limit=1,
        )

        self.assertEqual(new_record.status, "draft")

    def test_ensure_kyc_record_no_duplicate_when_active_exists(self):
        """Test that ensure_kyc_record does not create a record when an active one
        already exists."""
        # Create the first record with 'draft' status (active)
        self.test_partner.ensure_kyc_record()

        # Get the initial record
        initial_records = self.env["res.partner.id_number"].search(
            [
                ("partner_id", "=", self.test_partner.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        )

        self.assertEqual(len(initial_records), 1)

        # Call the API function again
        self.test_partner.ensure_kyc_record()

        # Verify that no duplicate was created (still has only 1 active record)
        final_records = self.env["res.partner.id_number"].search(
            [
                ("partner_id", "=", self.test_partner.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        )

        self.assertEqual(len(final_records), 1)

    def test_ensure_kyc_record_creates_when_expired_exists(self):
        """Test that ensure_kyc_record creates a record when only expired records
        exist."""
        # Create an expired record
        identification_model = self.env["res.partner.id_number"]
        identification_model.create(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-EXPIRED-TEST",
                "status": "close",
            }
        )

        initial_count = self.env["res.partner.id_number"].search_count(
            [
                ("partner_id", "=", self.test_partner.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        )
        self.assertEqual(initial_count, 1)

        # Call the API function - should create a new record since existing one is
        # expired
        self.test_partner.ensure_kyc_record()

        # Verify that a new record was created (now has 2 records total)
        final_count = self.env["res.partner.id_number"].search_count(
            [
                ("partner_id", "=", self.test_partner.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        )

        self.assertEqual(final_count, 2)

    def test_ensure_kyc_record_multiple_scenarios(self):
        """Test ensure_kyc_record with different status scenarios."""
        test_partner_multi = self.env["res.partner"].create(
            {
                "name": "Test Partner Multi",
                "email": "test.multi@example.com",
            }
        )

        identification_model = self.env["res.partner.id_number"]

        # Scenario 1: Add a 'close' record, then ensure_kyc_record should create new one
        identification_model.create(
            {
                "partner_id": test_partner_multi.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-CLOSE-TEST",
                "status": "close",
            }
        )

        initial_count = self.env["res.partner.id_number"].search_count(
            [
                ("partner_id", "=", test_partner_multi.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        )
        self.assertEqual(initial_count, 1)

        test_partner_multi.ensure_kyc_record()  # Should create new record
        count_after_ensure = self.env["res.partner.id_number"].search_count(
            [
                ("partner_id", "=", test_partner_multi.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        )
        self.assertEqual(count_after_ensure, 2)

        # Scenario 2: Add an 'open' record, then ensure_kyc_record should NOT create
        # new one
        test_partner_multi2 = self.env["res.partner"].create(
            {
                "name": "Test Partner Multi 2",
                "email": "test.multi2@example.com",
            }
        )

        identification_model.create(
            {
                "partner_id": test_partner_multi2.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-OPEN-TEST",
                "status": "open",
            }
        )

        initial_count2 = self.env["res.partner.id_number"].search_count(
            [
                ("partner_id", "=", test_partner_multi2.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        )
        self.assertEqual(initial_count2, 1)

        test_partner_multi2.ensure_kyc_record()  # Should NOT create new record
        count_after_ensure2 = self.env["res.partner.id_number"].search_count(
            [
                ("partner_id", "=", test_partner_multi2.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        )
        self.assertEqual(count_after_ensure2, 1)

    def test_button_visibility_conditions(self):
        """Test the visibility conditions for the Request KYC button."""
        # Initially, no KYC records exist, so button should be visible
        # (This is tested indirectly by testing the functions that implement the logic)

        # Create a 'draft' status record
        self.test_partner.action_request_kyc()

        # Now the button should be hidden (tested by trying to call the function
        # and expect error)
        with self.assertRaises(odoo.exceptions.UserError):
            self.test_partner.action_request_kyc()

        # Create a running status record with a different partner for testing
        partner2 = self.env["res.partner"].create(
            {
                "name": "Test Partner 2 for KYC",
                "email": "test2.kyc@example.com",
            }
        )

        identification_model = self.env["res.partner.id_number"]
        identification_model.create(
            {
                "partner_id": partner2.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-RUNNING-TEST",
                "status": "open",
            }
        )

        # With a running status, the button should be hidden
        with self.assertRaises(odoo.exceptions.UserError):
            partner2.action_request_kyc()

    def test_button_visibility_computed_field(self):
        """Test the computed field show_kyc_button for different scenarios."""
        # Initially, no KYC records - button should be visible (show_kyc_button = True)
        self.assertTrue(self.test_partner.show_kyc_button)

        # Create a draft status record - button should be hidden
        self.test_partner.action_request_kyc()
        # Reload the partner to get the updated computed field
        self.test_partner.invalidate_recordset()
        partner_reloaded = self.test_partner.browse(self.test_partner.id)
        self.assertFalse(partner_reloaded.show_kyc_button)

        # Create a new partner with pending status - button should be hidden
        partner_pending = self.env["res.partner"].create(
            {
                "name": "Test Partner Pending",
                "email": "test.pending@example.com",
            }
        )
        identification_model = self.env["res.partner.id_number"]
        identification_model.create(
            {
                "partner_id": partner_pending.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-PENDING-TEST",
                "status": "pending",
            }
        )
        partner_pending.invalidate_recordset()
        partner_pending_reloaded = partner_pending.browse(partner_pending.id)
        self.assertFalse(partner_pending_reloaded.show_kyc_button)

        # Create a new partner with close status - button should be visible
        partner_close = self.env["res.partner"].create(
            {
                "name": "Test Partner Close",
                "email": "test.close@example.com",
            }
        )
        identification_model.create(
            {
                "partner_id": partner_close.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-CLOSE-TEST",
                "status": "close",
            }
        )
        partner_close.invalidate_recordset()
        partner_close_reloaded = partner_close.browse(partner_close.id)
        self.assertTrue(partner_close_reloaded.show_kyc_button)

    def test_action_request_kyc_ensure_single_record(self):
        """Test that action_request_kyc works correctly with single record."""
        # Test that the method properly calls ensure_one()
        partners = self.test_partner | self.env["res.partner"].create(
            {
                "name": "Another Test Partner",
                "email": "another.test@example.com",
            }
        )

        # Calling the action on multiple records should raise an error
        with self.assertRaises(ValueError):
            partners.action_request_kyc()

    def test_ensure_kyc_record_idempotency(self):
        """Test that ensure_kyc_record is idempotent when record exists."""
        # Call ensure_kyc_record multiple times - should not create duplicates
        initial_count = self.env["res.partner.id_number"].search_count(
            [
                ("partner_id", "=", self.test_partner.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        )

        # First call - creates the record
        self.test_partner.ensure_kyc_record()

        # Second call - should not create a duplicate
        self.test_partner.ensure_kyc_record()

        final_count = self.env["res.partner.id_number"].search_count(
            [
                ("partner_id", "=", self.test_partner.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        )

        # Should have created only one record
        self.assertEqual(final_count, initial_count + 1)

    def test_multiple_status_scenarios_for_button_visibility(self):
        """Test all possible status combinations for button visibility."""
        # Create a new partner to test various scenarios
        test_partner_3 = self.env["res.partner"].create(
            {
                "name": "Test Partner 3",
                "email": "test3@example.com",
            }
        )

        # Initially, with no records, button should be visible
        self.assertTrue(test_partner_3.show_kyc_button)

        # Test each status combination

        # Test with 'open' (Running) status only - button should be hidden
        identification_model = self.env["res.partner.id_number"]
        identification_model.create(
            {
                "partner_id": test_partner_3.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-OPEN-TEST",
                "status": "open",
            }
        )
        test_partner_3.invalidate_recordset()
        reloaded_partner = test_partner_3.browse(test_partner_3.id)
        self.assertFalse(reloaded_partner.show_kyc_button)

        # Clean up for next test
        identification_model.search(
            [
                ("partner_id", "=", test_partner_3.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        ).unlink()

        # Test with 'pending' (To Renew) status only - button should be hidden
        identification_model.create(
            {
                "partner_id": test_partner_3.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-PENDING-TEST",
                "status": "pending",
            }
        )
        test_partner_3.invalidate_recordset()
        reloaded_partner = test_partner_3.browse(test_partner_3.id)
        self.assertFalse(reloaded_partner.show_kyc_button)

        # Clean up for next test
        identification_model.search(
            [
                ("partner_id", "=", test_partner_3.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        ).unlink()

        # Test with 'close' (Expired) status only - button should be visible
        identification_model.create(
            {
                "partner_id": test_partner_3.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-CLOSE-TEST",
                "status": "close",
            }
        )
        test_partner_3.invalidate_recordset()
        reloaded_partner = test_partner_3.browse(test_partner_3.id)
        self.assertTrue(reloaded_partner.show_kyc_button)

    def test_kyc_valid_until_computed_field_with_valid_dates(self):
        """Test the kyc_valid_until computed field when records have valid dates."""
        # Create KYC record with a valid_until date
        identification_model = self.env["res.partner.id_number"]
        identification_model.create(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-TEST-WITH-DATE",
                "status": "open",
                "valid_until": "2025-12-31",  # Set a future date
            }
        )

        # Reload partner to get updated computed field
        self.test_partner.invalidate_recordset()
        reloaded_partner = self.test_partner.browse(self.test_partner.id)

        # Should have a valid_until date
        self.assertIsNotNone(reloaded_partner.kyc_valid_until)
        self.assertEqual(
            reloaded_partner.kyc_valid_until, fields.Date.from_string("2025-12-31")
        )

    def test_kyc_valid_until_computed_field_multiple_records(self):
        """Test the kyc_valid_until computed field with multiple records
        to get min date."""
        identification_model = self.env["res.partner.id_number"]

        # Create multiple KYC records with different valid_until dates
        identification_model.create(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-TEST-DATE1",
                "status": "open",
                "valid_until": "2025-12-31",  # Later date
            }
        )

        identification_model.create(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-TEST-DATE2",
                "status": "open",
                "valid_until": "2025-06-15",  # Earlier date - should be the min
            }
        )

        # Reload partner to get updated computed field
        self.test_partner.invalidate_recordset()
        reloaded_partner = self.test_partner.browse(self.test_partner.id)

        # Should have the minimum (earliest) valid_until date
        self.assertIsNotNone(reloaded_partner.kyc_valid_until)
        self.assertEqual(
            reloaded_partner.kyc_valid_until, fields.Date.from_string("2025-06-15")
        )

    def test_kyc_valid_until_computed_field_no_open_records(self):
        """Test the kyc_valid_until computed field when no open records exist."""
        # Create a KYC record but with 'draft' status (not 'open')
        identification_model = self.env["res.partner.id_number"]
        identification_model.create(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-TEST-DRAFT",
                "status": "draft",  # Not 'open' status
            }
        )

        # Reload partner to get updated computed field
        self.test_partner.invalidate_recordset()
        reloaded_partner = self.test_partner.browse(self.test_partner.id)

        # Should be False since there are no 'open' status records
        self.assertFalse(reloaded_partner.kyc_valid_until)

    def test_kyc_valid_until_computed_field_open_records_without_dates(self):
        """Test the kyc_valid_until computed field when open records
        have no valid_until dates."""
        identification_model = self.env["res.partner.id_number"]

        # Create KYC record with 'open' status but no valid_until date
        identification_model.create(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-TEST-NO-DATE",
                "status": "open",  # Open status but no valid_until
            }
        )

        # Reload partner to get updated computed field
        self.test_partner.invalidate_recordset()
        reloaded_partner = self.test_partner.browse(self.test_partner.id)

        # Should be False since there are no valid_until dates in open records
        self.assertFalse(reloaded_partner.kyc_valid_until)

    def test_kyc_valid_until_computed_field_mixed_records(self):
        """Test the kyc_valid_until computed field with mixed records
        (some with dates, some without)."""
        identification_model = self.env["res.partner.id_number"]

        # Create one record with valid_until and one without
        identification_model.create(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-TEST-WITH-DATE",
                "status": "open",
                "valid_until": "2025-12-31",
            }
        )

        identification_model.create(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-TEST-NO-DATE",
                "status": "open",
                # No valid_until field
            }
        )

        # Reload partner to get updated computed field
        self.test_partner.invalidate_recordset()
        reloaded_partner = self.test_partner.browse(self.test_partner.id)

        # Should have the valid_until from the record that has it
        self.assertIsNotNone(reloaded_partner.kyc_valid_until)
        self.assertEqual(
            reloaded_partner.kyc_valid_until, fields.Date.from_string("2025-12-31")
        )

    def test_show_kyc_button_with_company_partner(self):
        """Test show_kyc_button computed field with company partner
        when child contacts disabled."""
        # First, disable child contacts on the KYC category
        self.kyc_category.enable_on_child_contacts = False

        # Create a company partner (should still be able to see button
        # regardless of enable_on_child_contacts)
        company_partner = self.env["res.partner"].create(
            {
                "name": "Company Partner",
                "email": "company@example.com",
                "is_company": True,  # Is a company
            }
        )

        # The button should be visible for companies even when
        # enable_on_child_contacts is False
        company_partner.invalidate_recordset()
        reloaded_company = company_partner.browse(company_partner.id)
        self.assertTrue(reloaded_company.show_kyc_button)

    def test_button_visibility_computed_field_with_disabled_child_contacts(self):
        """Test the computed field show_kyc_button when child contacts are disabled."""
        # First, disable child contacts on the KYC category
        self.kyc_category.enable_on_child_contacts = False

        # Create a non-company partner (individual contact)
        individual_contact = self.env["res.partner"].create(
            {
                "name": "Individual Contact",
                "email": "individual@example.com",
                "is_company": False,  # Not a company
            }
        )

        # The button should be hidden for individual contacts when
        # enable_on_child_contacts is False
        individual_contact.invalidate_recordset()
        reloaded_contact = individual_contact.browse(individual_contact.id)
        self.assertFalse(reloaded_contact.show_kyc_button)

    def test_button_visibility_computed_field_with_enabled_child_contacts(self):
        """Test the computed field show_kyc_button when child contacts are enabled."""
        # Ensure child contacts are enabled on the KYC category (default)
        self.kyc_category.enable_on_child_contacts = True

        # Create a non-company partner (individual contact)
        individual_contact = self.env["res.partner"].create(
            {
                "name": "Individual Contact",
                "email": "individual@example.com",
                "is_company": False,  # Not a company
            }
        )

        # The button should be visible for individual contacts when
        # enable_on_child_contacts is True
        individual_contact.invalidate_recordset()
        reloaded_contact = individual_contact.browse(individual_contact.id)
        self.assertTrue(reloaded_contact.show_kyc_button)

    def test_kyc_valid_until_computed_field_empty_sequence_edge_case(self):
        """Test that kyc_valid_until doesn't fail when open records exist
        but none have valid_until."""
        # Create multiple open records without valid_until dates
        # to test the min() edge case
        identification_model = self.env["res.partner.id_number"]

        identification_model.create(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-TEST-NO-DATE-1",
                "status": "open",
                # No valid_until
            }
        )

        identification_model.create(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-TEST-NO-DATE-2",
                "status": "open",
                # No valid_until
            }
        )

        # This should not raise an error and should return False
        self.test_partner.invalidate_recordset()
        reloaded_partner = self.test_partner.browse(self.test_partner.id)

        # Should be False since no records have valid_until dates
        self.assertFalse(reloaded_partner.kyc_valid_until)

    def test_action_request_kyc_with_custom_sequence(self):
        """Test action_request_kyc creates record with proper sequence."""
        # Remove any existing KYC records first
        existing_records = self.env["res.partner.id_number"].search(
            [
                ("partner_id", "=", self.test_partner.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        )
        existing_records.unlink()

        # Call action_request_kyc
        self.test_partner.action_request_kyc()

        # Check that a record was created
        kyc_records = self.env["res.partner.id_number"].search(
            [
                ("partner_id", "=", self.test_partner.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        )

        self.assertEqual(len(kyc_records), 1)
        self.assertEqual(kyc_records[0].status, "draft")
        # The ID Number is auto-assigned from the KYC sequence (prefix "KYC").
        self.assertTrue(kyc_records[0].name)
        self.assertTrue(kyc_records[0].name.startswith("KYC"))

    def test_ensure_kyc_record_when_none_exist(self):
        """Test ensure_kyc_record creates record when none exists."""
        # Remove any existing KYC records first
        existing_records = self.env["res.partner.id_number"].search(
            [
                ("partner_id", "=", self.test_partner.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        )
        existing_records.unlink()

        # Call ensure_kyc_record
        self.test_partner.ensure_kyc_record()

        # Check that a record was created
        kyc_records = self.env["res.partner.id_number"].search(
            [
                ("partner_id", "=", self.test_partner.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        )

        self.assertEqual(len(kyc_records), 1)
        self.assertEqual(kyc_records[0].status, "draft")

    def test_ensure_kyc_record_when_exists_with_active_status(self):
        """Test ensure_kyc_record does nothing when active record exists."""
        # Create an existing 'open' status record
        identification_model = self.env["res.partner.id_number"]
        identification_model.create(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-EXISTING-TEST",
                "status": "open",
            }
        )

        # Count existing records
        initial_count = self.env["res.partner.id_number"].search_count(
            [
                ("partner_id", "=", self.test_partner.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        )

        # Call ensure_kyc_record - should not create a new record
        self.test_partner.ensure_kyc_record()

        # Count should remain the same
        final_count = self.env["res.partner.id_number"].search_count(
            [
                ("partner_id", "=", self.test_partner.id),
                ("category_id", "=", self.kyc_category.id),
            ]
        )

        self.assertEqual(initial_count, final_count)

    def test_action_view_kyc_records(self):
        """Test action_view_kyc_records returns proper action."""
        # Create a KYC record first
        identification_model = self.env["res.partner.id_number"]
        identification_model.create(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-VIEW-TEST",
                "status": "open",
            }
        )

        # Call action_view_kyc_records
        action = self.test_partner.action_view_kyc_records()

        # Check the action structure
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "res.partner.id_number")
        self.assertIn("domain", action)

        # Check that domain contains partner_id filter
        domain_has_partner = any(
            isinstance(d, (list, tuple))
            and len(d) >= 3
            and d[0] == "partner_id"
            and d[1] == "="
            and d[2] == self.test_partner.id
            for d in action["domain"]
        )
        self.assertTrue(domain_has_partner)

    def test_kyc_valid_until_with_expired_and_active_records(self):
        """Test kyc_valid_until with mix of expired and active records."""
        identification_model = self.env["res.partner.id_number"]

        # Create an expired record (close status) with a date
        identification_model.create(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-EXPIRED-TEST",
                "status": "close",  # Not 'open' status, should be ignored
                "valid_until": "2020-01-01",  # Past date
            }
        )

        # Create an open record with a future date
        identification_model.create(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.kyc_category.id,
                "name": "KYC-ACTIVE-TEST",
                "status": "open",  # This one should be considered
                "valid_until": "2025-12-31",  # Future date
            }
        )

        # Reload partner to get updated computed field
        self.test_partner.invalidate_recordset()
        reloaded_partner = self.test_partner.browse(self.test_partner.id)

        # Should only consider 'open' status records
        self.assertIsNotNone(reloaded_partner.kyc_valid_until)
        expected_date = fields.Date.from_string("2025-12-31")
        self.assertEqual(reloaded_partner.kyc_valid_until, expected_date)

    def test_button_visibility_with_multiple_partners(self):
        """Test show_kyc_button computed field with multiple partners at once."""
        # Create multiple partners
        partner1 = self.env["res.partner"].create(
            {
                "name": "Partner 1",
                "email": "partner1@example.com",
            }
        )

        partner2 = self.env["res.partner"].create(
            {
                "name": "Partner 2",
                "email": "partner2@example.com",
            }
        )

        # Get multiple partners at once to test computed field batch processing
        partners = partner1 | partner2

        # All should have button visible initially (no KYC records)
        partners.invalidate_recordset()
        for partner in partners:
            self.assertTrue(partner.show_kyc_button)

    def test_ensure_kyc_record_batch_processing(self):
        """Test ensure_kyc_record works with multiple partners."""
        # Create multiple partners
        partner1 = self.env["res.partner"].create(
            {
                "name": "Batch Partner 1",
                "email": "batch1@example.com",
            }
        )

        partner2 = self.env["res.partner"].create(
            {
                "name": "Batch Partner 2",
                "email": "batch2@example.com",
            }
        )

        # Remove any existing KYC records for these partners
        existing_records = self.env["res.partner.id_number"].search(
            [
                ("partner_id", "in", [partner1.id, partner2.id]),
                ("category_id", "=", self.kyc_category.id),
            ]
        )
        existing_records.unlink()

        # Apply ensure_kyc_record to multiple partners at once
        partners = partner1 | partner2
        partners.ensure_kyc_record()

        # Each partner should now have a KYC record
        for partner in partners:
            partner_records = self.env["res.partner.id_number"].search(
                [
                    ("partner_id", "=", partner.id),
                    ("category_id", "=", self.kyc_category.id),
                ]
            )
            self.assertEqual(len(partner_records), 1)
            self.assertEqual(partner_records[0].status, "draft")
