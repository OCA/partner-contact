from datetime import datetime, timedelta

from freezegun import freeze_time

from odoo.tests.common import tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("post_install", "-at_install")
class TestIdentificationAutomation(BaseCommon):
    def setUp(self):
        super().setUp()

        # Create a test partner for issuer
        self.test_issuer = self.env["res.partner"].create(
            {
                "name": "Test Issuer",
            }
        )

        # Create a test partner
        self.test_partner = self.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )

        # Create a category with default values
        self.category = self.env["res.partner.id_category"].create(
            {
                "code": "test_license",
                "name": "Test License",
                "default_issuer_id": self.test_issuer.id,
                "default_validity_number": 30,
                "default_validity_unit": "days",
                "renewal_lead_number": 5,
                "renewal_lead_unit": "days",
            }
        )

        # Create identification number record
        self.identification = self.env["res.partner.id_number"].create(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.category.id,
                "name": "TEST123456",
                "valid_from": "2023-01-01",
            }
        )

    def test_onchange_defaults(self):
        """Test that the onchange method sets default values correctly"""
        # Test the onchange method by simulating form interaction
        identification = self.env["res.partner.id_number"].new(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.category.id,
                "name": "TEST987654",
                "valid_from": "2023-01-01",
            }
        )

        # Simulate onchange
        identification._onchange_category_defaults()

        # Check that default issuer is set
        self.assertEqual(identification.partner_issued_id, self.test_issuer)

        # Check that validity end is calculated correctly (30 days from start)
        expected_end = datetime(2023, 1, 1) + timedelta(days=30)
        self.assertEqual(identification.valid_until, expected_end.date())

    def test_status_expired(self):
        """Test that expired documents are properly marked as expired"""
        # Set validity end to a past date
        self.identification.write(
            {
                "valid_until": "2022-12-31",
                "status": "open",  # Use 'open' instead of 'running'
            }
        )

        # Run status update with frozen time in the future
        with freeze_time("2023-02-01"):
            self.identification._run_automatic_status_update()

        # Check that the document is marked as expired
        self.identification = self.identification.browse(self.identification.id)
        self.assertEqual(self.identification.status, "close")  # Use 'close' not 'exp'

    def test_status_to_renew(self):
        """Test that documents approaching expiry are marked as to_renew"""
        # Category has renewal_lead of 5 days, validity is 30 days from start
        # So anything within 5 days of expiry should be marked as pending
        # Start date is 2023-01-01, end date = 2023-01-31 (30 days later)
        # So anything 5 days before end date (2023-01-26) and before today = 'pending'

        # Set valid_until to allow expiry in 3 days from "today" (2023-01-28)
        self.identification.write(
            {
                "valid_from": "2023-01-01",
                "valid_until": "2023-01-28",  # Only 3 days from "today" (2023-01-25)
                "status": "open",  # Use 'open' instead of 'running'
            }
        )

        # Run status update - should trigger 'pending' within 5 days of expiry
        with freeze_time("2023-01-25"):
            self.identification._run_automatic_status_update()

        # Check that the document is marked as pending
        self.identification = self.identification.browse(self.identification.id)
        self.assertEqual(self.identification.status, "pending")  # Use 'pend' not 'tor'

    def test_status_running(self):
        """Test that valid documents are marked as running"""
        # Set validity period that is currently valid
        self.identification.write(
            {"valid_from": "2023-01-01", "valid_until": "2023-12-31", "status": "draft"}
        )

        # Run status update with current date in the valid range
        with freeze_time("2023-06-01"):
            self.identification._run_automatic_status_update()

        # Check that the document is marked as running (open)
        self.identification = self.identification.browse(self.identification.id)
        self.assertEqual(self.identification.status, "open")  # Use 'open' not 'running'

    def test_status_not_updated_for_final_states(self):
        """Test that final states like expired and cancelled aren't changed auto"""
        # Mark document as expired (close)
        self.identification.write(
            {
                "valid_until": "2022-01-01",
                "status": "close",  # Use 'close' instead of 'expired'
            }
        )

        # Run status update
        with freeze_time("2023-06-01"):
            self.identification._run_automatic_status_update()

        # Check that status remains close
        self.identification = self.identification.browse(self.identification.id)
        self.assertEqual(self.identification.status, "close")

        # Mark doc as cancelled - orig module doesn't have 'cancelled' status,
        # test the actual final state which is 'close'
        self.identification.write({"status": "close"})

        # Run status update
        with freeze_time("2023-06-01"):
            self.identification._run_automatic_status_update()

        # Check that status remains close
        self.identification = self.identification.browse(self.identification.id)
        self.assertEqual(self.identification.status, "close")

    def test_onchange_defaults_without_validity_start(self):
        """Test onchange when no validity start is provided"""
        identification = self.env["res.partner.id_number"].new(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.category.id,
                "name": "TEST987655",
                "valid_from": False,
            }
        )

        # Simulate onchange
        identification._onchange_category_defaults()

        # Check that default issuer is set even without valid_from
        self.assertEqual(identification.partner_issued_id, self.test_issuer)
        # But validity_until should not be set since valid_from is False
        self.assertFalse(identification.valid_until)

    def test_onchange_defaults_without_category(self):
        """Test onchange when no category is provided"""
        identification = self.env["res.partner.id_number"].new(
            {
                "partner_id": self.test_partner.id,
                "category_id": False,
                "name": "TEST987657",
                "valid_from": "2023-01-01",
            }
        )

        # Simulate onchange
        identification._onchange_category_defaults()

        # Check that no defaults are set when category is False
        self.assertFalse(identification.partner_issued_id)
        # The valid_from field is stored as a date object, not string
        expected_date = datetime(2023, 1, 1).date()
        self.assertEqual(identification.valid_from, expected_date)

    def test_onchange_defaults_with_weeks_unit(self):
        """Test onchange with weeks validity unit"""
        # Create category with weeks unit
        category_weeks = self.env["res.partner.id_category"].create(
            {
                "code": "test_license_weeks",
                "name": "Test License Weeks",
                "default_issuer_id": self.test_issuer.id,
                "default_validity_number": 2,
                "default_validity_unit": "weeks",
                "renewal_lead_number": 1,
                "renewal_lead_unit": "days",
            }
        )

        identification = self.env["res.partner.id_number"].new(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_weeks.id,
                "name": "TEST987658",
                "valid_from": "2023-01-01",
            }
        )

        # Simulate onchange
        identification._onchange_category_defaults()

        # Check that default issuer is set
        self.assertEqual(identification.partner_issued_id, self.test_issuer)

        # Check that validity end is calculated correctly (2 weeks from start)
        expected_end = datetime(2023, 1, 1).date() + timedelta(weeks=2)
        self.assertEqual(identification.valid_until, expected_end)

    def test_onchange_defaults_with_months_unit(self):
        """Test onchange with months validity unit and edge cases"""
        # Create category with months unit
        category_months = self.env["res.partner.id_category"].create(
            {
                "code": "test_license_months",
                "name": "Test License Months",
                "default_issuer_id": self.test_issuer.id,
                "default_validity_number": 1,
                "default_validity_unit": "months",
                "renewal_lead_number": 1,
                "renewal_lead_unit": "days",
            }
        )

        # Test with Jan 31 - edge case for month overflow
        identification = self.env["res.partner.id_number"].new(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_months.id,
                "name": "TEST987659",
                "valid_from": "2023-01-31",  # Jan 31
            }
        )

        # Simulate onchange - Jan 31 + 1 month should become Feb 28
        identification._onchange_category_defaults()

        # Check that default issuer is set
        self.assertEqual(identification.partner_issued_id, self.test_issuer)

        # Expected end date should be Feb 28, 2023
        expected_end = datetime(2023, 2, 28).date()
        self.assertEqual(identification.valid_until, expected_end)

    def test_onchange_defaults_with_years_unit(self):
        """Test onchange with years validity unit and leap year handling"""
        # Create category with years unit
        category_years = self.env["res.partner.id_category"].create(
            {
                "code": "test_license_years",
                "name": "Test License Years",
                "default_issuer_id": self.test_issuer.id,
                "default_validity_number": 1,
                "default_validity_unit": "years",
                "renewal_lead_number": 1,
                "renewal_lead_unit": "days",
            }
        )

        # Test with Feb 29 leap year - should handle leap year edge case
        identification_leap = self.env["res.partner.id_number"].new(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_years.id,
                "name": "TEST987660",
                "valid_from": "2024-02-29",  # Leap year Feb 29
            }
        )

        # Simulate onchange - Feb 29, 2024 + 1 year should become Feb 28, 2025
        identification_leap._onchange_category_defaults()

        # Check that default issuer is set
        self.assertEqual(identification_leap.partner_issued_id, self.test_issuer)

        # Expected end date should be Feb 28, 2025 (since 2025 is not a leap year)
        expected_end = datetime(2025, 2, 28).date()
        self.assertEqual(identification_leap.valid_until, expected_end)

        # Test normal case without leap year issues
        identification_normal = self.env["res.partner.id_number"].new(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_years.id,
                "name": "TEST987661",
                "valid_from": "2023-03-15",  # Normal date
            }
        )

        identification_normal._onchange_category_defaults()

        # Expected end date should be Mar 15, 2024
        expected_end_normal = datetime(2024, 3, 15).date()
        self.assertEqual(identification_normal.valid_until, expected_end_normal)

    def test_onchange_defaults_with_zero_duration(self):
        """Test onchange when validity duration is zero (edge case)"""
        # Create category with zero duration - this tests the case where
        # validity calculation results in no change to the start date
        category_zero = self.env["res.partner.id_category"].create(
            {
                "code": "test_license_zero",
                "name": "Test License Zero",
                "default_issuer_id": self.test_issuer.id,
                "default_validity_number": 0,  # Zero duration
                "default_validity_unit": "days",  # Using days with zero
                "renewal_lead_number": 1,
                "renewal_lead_unit": "days",
            }
        )

        # Create an identification with valid_until already set and test what happens
        # when we call onchange
        identification = self.env["res.partner.id_number"].new(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_zero.id,
                "name": "TEST987662",
                "valid_from": datetime(2023, 1, 1).date(),
                "valid_until": datetime(
                    2023, 1, 15
                ).date(),  # Initially set to a different date
            }
        )

        # Call the onchange method to populate the defaults
        identification._onchange_category_defaults()

        # Check that default issuer is set
        self.assertEqual(identification.partner_issued_id, self.test_issuer)

        # With 0 days duration, valid_until should be set to valid_from (2023-01-01),
        # since 0 days validity means it expires the same day it starts
        self.assertEqual(identification.valid_until, datetime(2023, 1, 1).date())

    def test_onchange_defaults_with_no_validity_dates(self):
        """Test onchange when no validity dates are specified"""
        # Create category normally
        category_normal = self.env["res.partner.id_category"].create(
            {
                "code": "test_license_normal",
                "name": "Test License Normal",
                "default_issuer_id": self.test_issuer.id,
                "default_validity_number": 10,
                "default_validity_unit": "days",
                "renewal_lead_number": 1,
                "renewal_lead_unit": "days",
            }
        )

        # Create identification without validity start date
        identification = self.env["res.partner.id_number"].new(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_normal.id,
                "name": "TEST987663",
                "valid_from": False,  # No start date
            }
        )

        # Simulate onchange - it should not try to calculate end date without start date
        identification._onchange_category_defaults()

        # Check that default issuer is set
        self.assertEqual(identification.partner_issued_id, self.test_issuer)

        # End date should not be set since there's no start date
        self.assertFalse(identification.valid_until)

    def test_renewal_with_different_units(self):
        """Test renewal calculation with different time units"""
        # Test with weeks
        category_weeks = self.env["res.partner.id_category"].create(
            {
                "code": "test_license_weeks",
                "name": "Test License Weeks",
                "default_issuer_id": self.test_issuer.id,
                "default_validity_number": 1,
                "default_validity_unit": "weeks",
                "renewal_lead_number": 1,
                "renewal_lead_unit": "weeks",
            }
        )

        identification = self.env["res.partner.id_number"].create(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_weeks.id,
                "name": "TEST_WEEKS",
                "valid_from": "2023-01-01",
                "valid_until": "2023-01-08",  # 1 week from start
            }
        )

        # Simulate time just before renewal period (end - 1 week = 2023-01-01,
        # so 2023-01-02 should be in renewal window)
        # Actually, the renewal cutoff would be 2023-01-08 - 1 week = 2023-01-01
        # So if we set time to 2023-01-02, it should be pending since today > cutoff
        # and today < expiry

        with freeze_time("2023-01-02"):
            identification._run_automatic_status_update()

        # Refresh the record and check status
        identification = identification.browse(identification.id)
        self.assertEqual(identification.status, "pending")

    def test_renewal_calculation_months_edge_case(self):
        """Test renewal calculation edge case with months"""
        # Create category with month-based renewal
        category_months = self.env["res.partner.id_category"].create(
            {
                "code": "test_license_months",
                "name": "Test License Months",
                "default_issuer_id": self.test_issuer.id,
                "default_validity_number": 1,
                "default_validity_unit": "months",
                "renewal_lead_number": 1,
                "renewal_lead_unit": "months",
            }
        )

        # Create ID that expires on Feb 28 (edge cases when subtracting months)
        identification = self.env["res.partner.id_number"].create(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_months.id,
                "name": "TEST_MONTHS",
                "valid_from": "2023-01-31",
                "valid_until": "2023-02-28",  # Feb 2023 only has 28 days
            }
        )

        # The renewal cutoff would be 2023-02-28 - 1 month = 2023-01-28
        # So if we're after Jan 28 but before Feb 28, it should be pending
        with freeze_time("2023-02-20"):
            identification._run_automatic_status_update()

        identification = identification.browse(identification.id)
        self.assertEqual(identification.status, "pending")

    def test_expired_but_already_pending(self):
        """Test that expired identification with pending status gets closed"""
        # Create an ID that should be marked as pending
        self.identification.write(
            {
                "valid_from": "2023-01-01",
                "valid_until": "2023-01-30",
                "status": "pending",  # Already pending
            }
        )

        # Simulate time after expiration
        with freeze_time("2023-02-01"):
            self.identification._run_automatic_status_update()

        # Refresh the record and check status - should be 'close' now
        self.identification = self.identification.browse(self.identification.id)
        self.assertEqual(self.identification.status, "close")

    def test_running_to_pending_transition(self):
        """Test transition from open to pending when entering renewal window"""
        # Create an ID that is currently valid (should be 'open')
        self.identification.write(
            {
                "valid_from": "2023-01-01",
                "valid_until": "2023-02-10",
                "status": "open",  # Currently running
            }
        )

        # Set time to when it should become pending (within renewal window)
        # Category has renewal_lead_number: 5 and renewal_lead_unit: 'days'
        # So renewal cutoff is 2023-02-10 - 5 days = 2023-02-05
        # With time 2023-02-06, it should be pending
        # (2023-02-05 < 2023-02-06 < 2023-02-10)
        with freeze_time("2023-02-06"):
            self.identification._run_automatic_status_update()

        # Refresh the record and check status - should be 'pending'
        self.identification = self.identification.browse(self.identification.id)
        self.assertEqual(self.identification.status, "pending")

    def test_no_renewal_settings(self):
        """Test behavior when category has no renewal settings"""
        # Create category with no renewal settings
        # Explicitly set renewal lead to 0 to indicate no renewal functionality
        category_no_renewal = self.env["res.partner.id_category"].create(
            {
                "code": "test_license_no_renewal",
                "name": "Test License No Renewal",
                "default_issuer_id": self.test_issuer.id,
                "default_validity_number": 30,
                "default_validity_unit": "days",
                # Explicitly disable renewal settings
                "renewal_lead_number": 0,
                "renewal_lead_unit": "days",
            }
        )

        identification = self.env["res.partner.id_number"].create(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_no_renewal.id,
                "name": "TEST_NO_RENEWAL",
                "valid_from": "2023-01-01",
                "valid_until": "2023-02-10",
                "status": "open",
            }
        )

        # Run status update - should handle gracefully without renewal settings
        # In this case, _calculate_renewal_cutoff will return valid_until_date
        # So renewal_cutoff (2023-02-10) < today (2023-02-05) is False
        # So it won't be marked as pending and will remain open (if it's in valid range)
        with freeze_time("2023-02-05"):  # Within validity but before expiry
            identification._run_automatic_status_update()

        identification = identification.browse(identification.id)
        # Should be 'open' since 2023-02-05 is within validity range
        # and not in renewal window (renewal_cutoff = expiry when no renewal settings)
        self.assertEqual(identification.status, "open")

    def test_no_validity_dates(self):
        """Test behavior when identification has no validity dates"""
        # Create identification without validity dates
        identification_no_dates = self.env["res.partner.id_number"].create(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.category.id,
                "name": "TEST_NO_DATES",
                "valid_from": False,
                "valid_until": False,
                "status": "draft",
            }
        )

        # Run status update - should not cause errors
        with freeze_time("2023-01-01"):
            identification_no_dates._run_automatic_status_update()

        # Refresh and check: should remain in original status since no validity dates
        identification_no_dates = identification_no_dates.browse(
            identification_no_dates.id
        )
        self.assertEqual(identification_no_dates.status, "draft")

    def test_renewal_cutoff_calculation_months_edge_cases(self):
        """Test renewal cutoff calculation for months with year underflow"""
        # Test the month underflow logic: month <= 0, year -= 1, month += 12
        category_months = self.env["res.partner.id_category"].create(
            {
                "code": "test_renewal_months",
                "name": "Test Renewal Months",
                "default_issuer_id": self.test_issuer.id,
                "renewal_lead_number": 15,  # 15 months
                "renewal_lead_unit": "months",  # Subtracting from expiry
            }
        )

        # Create identification with expiry in early year so subtracting 15 months
        # goes to previous year
        # Expiry on 2023-02-15, minus 15 months = 1 month in previous year
        # = 2022-11-15
        identification = self.env["res.partner.id_number"].create(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_months.id,
                "name": "TEST_RENEWAL_MONTHS",
                "valid_from": "2022-01-01",
                "valid_until": "2023-02-15",  # Feb 15, 2023
                "status": "open",
            }
        )

        # Run status update
        with freeze_time("2022-12-01"):  # After the calculated renewal cutoff date
            identification._run_automatic_status_update()

        # Refresh and check status - should be 'pending' because renewal cutoff is
        # 2023-02-15 minus 15 months = May 15, 2022. So 2022-12-01 > 2022-05-15
        # and < 2023-02-15
        identification = identification.browse(identification.id)
        self.assertEqual(identification.status, "pending")

    def test_renewal_cutoff_calculation_years_edge_cases(self):
        """Test renewal cutoff calculation for years with leap year handling"""
        # Test the year calculation with leap year edge case
        category_years = self.env["res.partner.id_category"].create(
            {
                "code": "test_renewal_years",
                "name": "Test Renewal Years",
                "default_issuer_id": self.test_issuer.id,
                "renewal_lead_number": 1,  # 1 year
                "renewal_lead_unit": "years",  # Subtracting from expiry
            }
        )

        # Create identification expiring on Feb 29 in a leap year
        # This should test the leap year handling in renewal cutoff calculation
        identification_leap = self.env["res.partner.id_number"].create(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_years.id,
                "name": "TEST_RENEWAL_LEAP",
                "valid_from": "2020-01-01",
                "valid_until": "2024-02-29",  # Feb 29, 2024 (leap year)
                "status": "open",
            }
        )

        # The renewal cutoff will be: 2024-02-29 minus 1 year = 2023-02-29
        # But 2023 is not a leap year, so it should become 2023-02-28
        # So if we check after 2023-02-28, it should be pending
        with freeze_time("2023-03-01"):  # After the renewal cutoff date
            identification_leap._run_automatic_status_update()

        # Refresh and check: should be 'pending' because today is after renewal cutoff
        identification_leap = identification_leap.browse(identification_leap.id)
        self.assertEqual(identification_leap.status, "pending")

        # Also test a normal case without leap year issues
        identification_normal = self.env["res.partner.id_number"].create(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_years.id,
                "name": "TEST_RENEWAL_NORMAL",
                "valid_from": "2022-01-01",
                "valid_until": "2024-03-15",  # March 15, 2024 (not a leap year issue)
                "status": "open",
            }
        )

        # Renewal cutoff: 2024-03-15 minus 1 year = 2023-03-15
        with freeze_time("2023-03-20"):  # After the renewal cutoff
            identification_normal._run_automatic_status_update()

        identification_normal = identification_normal.browse(identification_normal.id)
        self.assertEqual(identification_normal.status, "pending")

    def test_renewal_calculation_with_category_without_settings(self):
        """Test renewal calculation when category doesn't have renewal settings"""
        # Create category without renewal lead configurations
        category_no_renewal = self.env["res.partner.id_category"].create(
            {
                "code": "test_no_renewal_settings",
                "name": "Test No Renewal Settings",
                "default_issuer_id": self.test_issuer.id,
                # Deliberately not setting renewal_lead_number and renewal_lead_unit
            }
        )

        # Create identification with this category
        identification = self.env["res.partner.id_number"].create(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_no_renewal.id,
                "name": "TEST_NO_RENEWAL_SETTINGS",
                "valid_from": "2023-01-01",
                "valid_until": "2023-12-31",  # Future date
                "status": "open",
            }
        )

        # Run status update - should handle gracefully when no renewal settings exist
        with freeze_time("2023-06-01"):
            identification._run_automatic_status_update()

        # Refresh and check: should still be open since no renewal window is defined
        identification = identification.browse(identification.id)
        self.assertEqual(identification.status, "open")

    def test_status_transitions_priority_correctness(self):
        """Test that status transitions happen in correct priority order"""
        # Create category with short renewal window to ensure the document will be
        # pending
        category_short_renewal = self.env["res.partner.id_category"].create(
            {
                "code": "test_short_renewal",
                "name": "Test Short Renewal",
                "default_issuer_id": self.test_issuer.id,
                "renewal_lead_number": 30,  # 30 days before expiry
                "renewal_lead_unit": "days",
            }
        )

        # Create identification that is currently valid but within renewal window
        identification = self.env["res.partner.id_number"].create(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_short_renewal.id,
                "name": "TEST_PRIORITY",
                "valid_from": "2023-01-01",
                "valid_until": "2023-06-15",  # Expires in near future
                "status": "open",
            }
        )

        # Run status update with time after renewal cutoff but before expiry
        # Renewal cutoff: 2023-06-15 - 30 days = 2023-05-16
        # Current time: 2023-06-01 (after cutoff, before expiry)
        with freeze_time("2023-06-01"):
            identification._run_automatic_status_update()

        # Should be 'pending' because in renewal window and not expired
        identification = identification.browse(identification.id)
        self.assertEqual(identification.status, "pending")

        # Change time to after expiry - should now be 'close' regardless of previous
        # 'pending'
        with freeze_time("2023-07-01"):
            identification._run_automatic_status_update()

        identification = identification.browse(identification.id)
        self.assertEqual(identification.status, "close")

    def test_running_status_when_not_in_renewal_window(self):
        """Test that valid IDs remain 'open' when not in renewal window"""
        # Create identification that is currently valid and not in renewal window
        identification = self.env["res.partner.id_number"].create(
            {
                "partner_id": self.test_partner.id,
                "category_id": self.category.id,  # Using default category
                "name": "TEST_RUNNING",
                "valid_from": "2023-01-01",
                "valid_until": "2025-12-31",  # Far future date
                "status": "draft",  # Starting with draft status
            }
        )

        # Run status update - should transition from draft to open
        with freeze_time("2023-06-01"):
            identification._run_automatic_status_update()

        identification = identification.browse(identification.id)
        self.assertEqual(identification.status, "open")

        # Run again - should remain open since not in renewal window or expired
        with freeze_time("2023-06-02"):
            identification._run_automatic_status_update()

        identification = identification.browse(identification.id)
        self.assertEqual(identification.status, "open")

    def test_category_with_default_validity_settings_years(self):
        """Test that category default validity settings in years work correctly"""
        # Create a category with default validity in years
        category_years = self.env["res.partner.id_category"].create(
            {
                "name": "Test Category Years",
                "code": "test_years",
                "default_issuer_id": self.test_issuer.id,
                "default_validity_number": 2,  # 2 years
                "default_validity_unit": "years",  # Years unit
            }
        )

        # Create an identification with valid_from date
        identification = self.env["res.partner.id_number"].create(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_years.id,
                "name": "TEST_DEFAULT_YEARS",
                "valid_from": "2023-01-01",
            }
        )

        # Verify that valid_until is set correctly (2 years from 2023-01-01)
        expected_valid_until = datetime(2025, 1, 1).date()
        self.assertEqual(identification.valid_until, expected_valid_until)

    def test_category_with_default_validity_settings_months(self):
        """Test that category default validity settings in months work correctly"""
        # Create a category with default validity in months
        category_months = self.env["res.partner.id_category"].create(
            {
                "name": "Test Category Months",
                "code": "test_months",
                "default_issuer_id": self.test_issuer.id,
                "default_validity_number": 6,  # 6 months
                "default_validity_unit": "months",  # Months unit
            }
        )

        # Create an identification with valid_from date
        identification = self.env["res.partner.id_number"].create(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_months.id,
                "name": "TEST_DEFAULT_MONTHS",
                "valid_from": "2023-01-31",  # End of January to test month edge cases
            }
        )

        # Verify that valid_until is calculated correctly (Jan 31 + 6 months = July 31)
        expected_valid_until = datetime(2023, 7, 31).date()
        self.assertEqual(identification.valid_until, expected_valid_until)

    def test_renewal_calculation_with_months_lead_time(self):
        """Test renewal calculation with months as lead time unit"""
        # Create category with renewal lead of 2 months
        category_months_lead = self.env["res.partner.id_category"].create(
            {
                "name": "Test Category Months Lead",
                "code": "test_months_lead",
                "default_issuer_id": self.test_issuer.id,
                "renewal_lead_number": 2,  # 2 months before expiry
                "renewal_lead_unit": "months",  # Months unit for renewal lead
            }
        )

        # Create identification expiring in 3 months
        identification = self.env["res.partner.id_number"].create(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_months_lead.id,
                "name": "TEST_RENEWAL_MONTHS_LEAD",
                "valid_from": "2023-01-01",
                "valid_until": "2023-04-01",  # April 1, 2023
            }
        )

        # Run status update after renewal cutoff (April 1 - 2 months = Feb 1)
        # So if current date is after Feb 1, it should be pending
        with freeze_time("2023-03-01"):  # After Feb 1, before Apr 1
            identification._run_automatic_status_update()

        # Verify that the status was updated correctly by the automated system
        identification = identification.browse(identification.id)
        self.assertEqual(identification.status, "pending")

    def test_renewal_calculation_with_weeks_lead_time(self):
        """Test renewal calculation with weeks as lead time unit"""
        # Create category with renewal lead of 3 weeks
        category_weeks_lead = self.env["res.partner.id_category"].create(
            {
                "name": "Test Category Weeks Lead",
                "code": "test_weeks_lead",
                "default_issuer_id": self.test_issuer.id,
                "renewal_lead_number": 3,  # 3 weeks before expiry
                "renewal_lead_unit": "weeks",  # Weeks unit for renewal lead
            }
        )

        # Create identification expiring in 4 weeks
        identification = self.env["res.partner.id_number"].create(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_weeks_lead.id,
                "name": "TEST_RENEWAL_WEEKS_LEAD",
                "valid_from": "2023-01-01",
                "valid_until": "2023-01-29",  # 29 days from start (approx. 4 weeks)
            }
        )

        # Run status update with time after renewal cutoff (Jan 29 - 3 weeks = Jan 8)
        # So if current date is after Jan 8, it should trigger pending status
        with freeze_time("2023-01-15"):  # After Jan 8, before Jan 29
            identification._run_automatic_status_update()

        # Verify that the status was updated correctly by the automated system
        identification = identification.browse(identification.id)
        self.assertEqual(identification.status, "pending")

    def test_renewal_calculation_with_days_lead_time(self):
        """Test renewal calculation with days as lead time unit"""
        # Create category with renewal lead of 10 days
        category_days_lead = self.env["res.partner.id_category"].create(
            {
                "name": "Test Category Days Lead",
                "code": "test_days_lead",
                "default_issuer_id": self.test_issuer.id,
                "renewal_lead_number": 10,  # 10 days before expiry
                "renewal_lead_unit": "days",  # Days unit for renewal lead
            }
        )

        # Create identification expiring in 15 days
        identification = self.env["res.partner.id_number"].create(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_days_lead.id,
                "name": "TEST_RENEWAL_DAYS_LEAD",
                "valid_from": "2023-01-01",
                "valid_until": "2023-01-16",  # 15 days from start
            }
        )

        # Run status update with time after renewal cutoff (Jan 16 - 10 days = Jan 6)
        # So if current date is after Jan 6, it should trigger pending status
        with freeze_time("2023-01-12"):  # After Jan 6, before Jan 16
            identification._run_automatic_status_update()

        # Verify that the status was updated correctly by the automated system
        identification = identification.browse(identification.id)
        self.assertEqual(identification.status, "pending")

    def test_no_renewal_calculation_when_lead_number_is_zero(self):
        """Test that no renewal calculation happens when lead number is zero"""
        # Create category with renewal lead number as 0 (disabled)
        category_no_renewal = self.env["res.partner.id_category"].create(
            {
                "name": "Test Category No Renewal",
                "code": "test_no_renewal",
                "default_issuer_id": self.test_issuer.id,
                "renewal_lead_number": 0,  # Zero disables renewal automation
                "renewal_lead_unit": "days",  # Unit doesn't matter when number is 0
            }
        )

        # Create identification that should normally trigger renewal
        identification = self.env["res.partner.id_number"].create(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_no_renewal.id,
                "name": "TEST_NO_RENEWAL_CALC",
                "valid_from": "2023-01-01",
                "valid_until": "2023-01-05",  # Expires in 5 days
            }
        )

        # Ensure status is initially 'draft' or 'open' to test renewal logic
        identification.write({"status": "open"})

        # Run status update that would normally trigger renewal
        # if renewal wasn't disabled
        with freeze_time("2023-01-04"):  # Close to expiry
            identification._run_automatic_status_update()

        # Verify that the status remains unchanged because
        # renewal is disabled (lead number is 0)
        identification = identification.browse(identification.id)
        self.assertEqual(identification.status, "open")  # Should remain open

    def test_onchange_method_with_different_validity_units(self):
        """Test onchange method works with all validity units"""
        # First test with days
        category_days = self.env["res.partner.id_category"].create(
            {
                "name": "Test Category Days",
                "code": "test_cat_days",
                "default_issuer_id": self.test_issuer.id,
                "default_validity_number": 5,
                "default_validity_unit": "days",
            }
        )

        identification_days = self.env["res.partner.id_number"].new(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_days.id,
                "name": "TEST_ONCHANGE_DAYS",
                "valid_from": "2023-01-01",
            }
        )

        identification_days._onchange_category_defaults()
        expected_date = datetime(2023, 1, 6).date()  # 5 days after Jan 1
        self.assertEqual(identification_days.valid_until, expected_date)

        # Test with weeks
        category_weeks = self.env["res.partner.id_category"].create(
            {
                "name": "Test Category Weeks",
                "code": "test_cat_weeks",
                "default_issuer_id": self.test_issuer.id,
                "default_validity_number": 2,
                "default_validity_unit": "weeks",
            }
        )

        identification_weeks = self.env["res.partner.id_number"].new(
            {
                "partner_id": self.test_partner.id,
                "category_id": category_weeks.id,
                "name": "TEST_ONCHANGE_WEEKS",
                "valid_from": "2023-01-01",
            }
        )

        identification_weeks._onchange_category_defaults()
        expected_date = datetime(2023, 1, 15).date()  # 2 weeks after Jan 1
        self.assertEqual(identification_weeks.valid_until, expected_date)
