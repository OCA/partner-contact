# Copyright 2021 Patrick Wilson <pwilson@opensourceintegrators.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.exceptions import ValidationError
from odoo.tests import common, tagged


@tagged("-at_install", "post_install")
class TestPartnerTierValidation(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Get res partner model
        cls.partner_model = cls.env.ref("base.model_res_partner")

        # Create users
        group_ids = cls.env.ref("base.group_system").ids
        group_ids.append(cls.env.ref("base.group_partner_manager").id)
        cls.test_user_1 = cls.env["res.users"].create(
            {
                "name": "John",
                "login": "test1",
                "groups_id": [(6, 0, group_ids)],
                "email": "test@example.com",
            }
        )

        # Create tier definition: example where only Company needs validation
        cls.TierDefinition = cls.env["tier.definition"]
        cls.TierDefinition.create(
            {
                "model_id": cls.partner_model.id,
                "review_type": "individual",
                "reviewer_id": cls.test_user_1.id,
                "definition_domain": "[('is_company','=',True)]",
            }
        )

    def test_tier_validation_model_name(self):
        self.assertIn(
            "res.partner", self.TierDefinition._get_tier_validation_model_names()
        )

    def test_validation_res_partner(self):
        """
        Case where new Contact requires validation
        """
        contact = self.env["res.partner"].create(
            {"name": "Company for test", "company_type": "company"}
        )
        # Since contact need validation, it should be inactive
        self.assertEqual(contact.state, "draft")

        # Assert an error shows if trying to make it active
        with self.assertRaises(ValidationError):
            contact.write({"state": "confirmed"})

        # Request and validate partner
        contact.request_validation()
        contact.with_user(self.test_user_1).validate_tier()
        contact.with_user(self.test_user_1).write({"state": "confirmed"})
        self.assertEqual(contact.state, "confirmed")

        # Change company type to retrigger validation
        contact.write({"company_type": "person", "is_company": False})
        self.assertEqual(contact.state, "draft")

    def test_no_validation_res_partner(self):
        """
        Case where new Contact does not require validation
        """
        contact = self.env["res.partner"].create(
            {"name": "Person for test", "company_type": "person"}
        )
        self.assertEqual(contact.state, "confirmed")
