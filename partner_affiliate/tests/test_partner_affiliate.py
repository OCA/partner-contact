# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
"""Tests for partner_affiliate."""
from odoo.tests import common


class TestPartnerAffiliate(common.TransactionCase):
    """Tests for partner_affiliate."""

    def setUp(self):
        super().setUp()
        self.partner_obj = self.env["res.partner"]
        self.first_company = self.partner_obj.create(
            {
                "name": "MyFirstCompanyForTheAffiliate",
                "type": "contact",
                "is_company": True,
                "street": "first company street",
            }
        )
        self.second_company = self.partner_obj.create(
            {
                "name": "MySecondCompanyForTheAffiliate",
                "type": "contact",
                "is_company": True,
                "street": "second company street",
            }
        )

    def test_change_parent_from_a_new_affiliate(self):
        """Check data integrity of the objects when an affiliate is given a new
        parent. So both objects keeps their data.
        """
        my_affiliate = self.partner_obj.create(
            {
                "name": "MyAffiliate",
                "is_company": True,
                "parent_id": self.first_company.id,
                "type": "affiliate",
                "street": "affiliate street",
            }
        )
        # Checks for data integrity in affiliate and his parent.
        self.assertTrue(my_affiliate, "Failed to create the new affiliate.")
        self.assertEqual(
            my_affiliate.type, "affiliate", "Check type must be 'affiliate'"
        )
        self.assertEqual(
            my_affiliate.parent_id.id,
            self.first_company.id,
            "Must be child of the parent defined in the setup",
        )
        self.assertEqual(
            my_affiliate.street,
            "affiliate street",
            "The street has not been correctly set.",
        )
        self.assertEqual(
            self.first_company.street,
            "first company street",
            "Unexpected change in parent street",
        )
        # Change the parent of the affiliate for the second one in the set-up.
        my_affiliate.parent_id = self.second_company.id
        my_affiliate.onchange_parent_id()
        # The parent has been changed. And is not the first one.
        self.assertEqual(my_affiliate.parent_id.id, self.second_company.id)
        # The affiliate keeps its data for the street (address). Not modified.
        self.assertEqual(
            my_affiliate.street,
            "affiliate street",
            "Affilliate street should not have changed",
        )
        # The data for the street of the first parent have not been changed.
        self.assertEqual(
            self.first_company.street,
            "first company street",
            "First company street should not have changed",
        )

    def test_new_affiliate_is_created_with_type_affiliate_by_default(self):
        """Check that the default value for 'type' defined by default in the view
        is set correctly when a new affiliate is created.
        """
        new_affiliate = self.partner_obj.with_context(
            {
                "default_parent_id": self.first_company.id,
                "default_is_company": True,
                "default_type": "affiliate",
            }
        ).create({"name": "MyTestAffiliate", "street": "affiliate street"})
        self.assertEqual(new_affiliate.type, "affiliate")

    def test_individual_changes_address_when_changing_parent_id(self):
        """Check that when changing the parent from an individual, it changes also
        the address keeping the expected behaviour.
        """
        my_individual = self.partner_obj.create(
            {
                "name": "MyIndividual",
                "parent_id": self.first_company.id,
                "type": "contact",
                "is_company": False,
                "street": "individual street",
            }
        )
        my_individual.parent_id = self.second_company.id
        my_individual.onchange_parent_id()
        # The parent has been changed.
        self.assertEqual(my_individual.parent_id.id, self.second_company.id)
        # The affiliate gets the address from the new parent.
        self.assertEqual(
            my_individual.street,
            "second company street",
            "Street of affiliate individual should heve been set to company street",
        )

    def test_company_keeps_address_when_changing_parent_id(self):
        """Check that when changing the parent from a company, it keeps its own
        address.
        """
        my_affiliate_company = self.partner_obj.create(
            {
                "name": "My Affiliate Company",
                "parent_id": self.first_company.id,
                "type": "contact",
                "is_company": True,
                "street": "affiliate_company street",
            }
        )
        my_affiliate_company.parent_id = self.second_company.id
        my_affiliate_company.onchange_parent_id()
        # The parent has been changed.
        self.assertEqual(my_affiliate_company.parent_id.id, self.second_company.id)
        # The affiliate should keep its own address.
        self.assertEqual(
            my_affiliate_company.street,
            "affiliate_company street",
            "Street of affiliate company should not have changed",
        )
        # Change of parent should not affect the type.
        self.assertEqual(
            my_affiliate_company.type, "affiliate", "Check type must remain 'affiliate'"
        )
