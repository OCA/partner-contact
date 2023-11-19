from odoo.tests import tagged

from ..consts import PREDEFINED_RULES
from .common import PartnerTweaksAccessCommon


@tagged("post_install", "-at_install", "standart")
class TestPartnerTweaksAccess(PartnerTweaksAccessCommon):
    def test_user_access_difference(self):
        """
        Check the search results are different for a user without access tweaks
        and a user with access tweaks.
        """
        result_without_tweaks = self.partner_model.with_user(
            self.user_without_tweaks_access
        ).search([])
        result_with_tweaks = self.partner_model.with_user(
            self.user_with_tweaks_access
        ).search([])

        # Ensure that the search results are not equal for the two users
        self.assertNotEqual(
            result_without_tweaks,
            result_with_tweaks,
            msg="The search results should not be equal",
        )

    def test_user_access_partner_categories(self):
        """Check the availability of users by partner categories"""

        # Ensure that the user does not have access to test_category1 initially
        initial_partners = self.partner_model.with_user(
            self.user_with_tweaks_access
        ).search([])
        self.assertNotIn(
            self.test_category1,
            initial_partners.mapped("category_id"),
            msg=(
                "The allowed user categories should not"
                "include the category #'{category}'"
            ).format(category=self.test_category1.id),
        )

        # Add test_category1 to the user's allowed categories
        self.user_with_tweaks_access.allowed_partner_category_ids = [
            (4, self.test_category1.id, False)
        ]

        # Check that the user now has access to test_category1
        updated_partners = self.partner_model.with_user(
            self.user_with_tweaks_access
        ).search([])
        self.assertIn(
            self.test_category1,
            updated_partners.mapped("category_id"),
            msg=(
                "The allowed user categories should"
                "include the category #'{category}'"
            ).format(category=self.test_category1.id),
        )

    def test_user_access_partner_countries(self):
        """Check the availability of users by partner countries and states"""

        # Check that the user initially doesn't have access
        # to test_country and test_country_state
        partners = self.partner_model.with_user(self.user_with_tweaks_access).search([])
        self.assertNotIn(
            self.country,
            partners.mapped("country_id"),
            msg=(
                "The allowed user countries should not include"
                "the country #'{country}'"
            ).format(country=self.country.id),
        )
        self.assertNotIn(
            self.country_state,
            partners.mapped("state_id"),
            msg=(
                "The allowed user states should not include" "the state #'{state}'"
            ).format(state=self.country_state.id),
        )

        # Update user to the appropriate group with access to countries and states
        self.user_with_tweaks_access.groups_id = [
            (4, self.env.ref("prt_partner_tweaks_access.prt_contact_regions").id)
        ]

        # Add test_country and test_country_state to the user's allowed countries and states
        self.user_with_tweaks_access.allowed_country_ids = [(4, self.country.id, False)]
        self.user_with_tweaks_access.allowed_country_state_ids = [
            (4, self.country_state.id, False)
        ]

        # Check that the user now has access to test_country and test_country_state
        partners = self.partner_model.with_user(self.user_with_tweaks_access).search([])
        self.assertIn(
            self.country,
            partners.mapped("country_id"),
            msg=(
                "The allowed user countries should include" "the country #'{country}'"
            ).format(country=self.country.id),
        )
        self.assertIn(
            self.country_state,
            partners.mapped("state_id"),
            msg=(
                "The allowed user states should include" "the state #'{state}'"
            ).format(state=self.country_state.id),
        )

    def test_predefined_rules_state(self):
        """
        Test that applying tweaks to user access rules activates predefined rules.
        """
        self.user_model.actived_predefined_rules_state()

        # Search for predefined rules
        rules = (
            self.env["ir.rule"]
            .with_context(active_test=False)
            .sudo()
            .search([("name", "in", PREDEFINED_RULES)])
        )

        # Check that rules are not empty
        self.assertGreater(len(rules), 0, msg="There should be predefined rules")

        # Check that all rules are active
        rules_active = rules.mapped("active")
        self.assertTrue(
            not all(rules_active), msg="All predefined rules should be active"
        )
