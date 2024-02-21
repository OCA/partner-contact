# Copyright 2021 Patrick Wilson <pwilson@opensourceintegrators.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.exceptions import ValidationError
from odoo.tests import common, tagged


@tagged("-at_install", "post_install")
class TestPartnerTierValidation(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create users
        group_user = cls.env.ref("base.group_user")
        group_contacts = cls.env.ref("base.group_partner_manager")
        group_approver = cls.env.ref("base.group_no_one")
        User = cls.env["res.users"]
        cls.user_employee = User.create(
            {
                "name": "Employee",
                "login": "empl1",
                "email": "empl1@example.com",
                "groups_id": (group_user | group_contacts).ids,
            }
        )
        cls.user_approver = User.create(
            {
                "name": "Approver",
                "login": "aprov1",
                "email": "approv1@example.com",
                "groups_id": (group_user | group_contacts | group_approver).ids,
            }
        )

        # Create tier definition: example where only Company needs validation
        cls.TierDefinition = cls.env["tier.definition"]
        cls.TierDefinition.create(
            {
                "model_id": cls.env.ref("base.model_res_partner").id,
                "review_type": "individual",
                "reviewer_id": cls.user_approver.id,
                "definition_domain": "[('is_company','=',True)]",
            }
        )

        # Setup Contact Stages: draft is the default
        Stage = cls.env["res.partner.stage"]
        Stage.search([("is_default", "=", True)]).write({"is_default": False})
        cls.stage_draft = Stage.search([("state", "=", "draft")], limit=1)
        cls.stage_draft.is_default = True
        cls.stage_confirmed = Stage.search([("state", "=", "confirmed")], limit=1)

    def test_tier_validation_model_name(self):
        self.assertIn(
            "res.partner", self.TierDefinition._get_tier_validation_model_names()
        )

    def test_validation_res_partner(self):
        """
        Case where new Contact requires validation
        """
        Partner = self.env["res.partner"]
        contact_vals = {"name": "Company for test", "company_type": "company"}
        contact = Partner.with_user(self.user_employee).create(contact_vals)
        self.assertEqual(contact.state, "draft")

        # Assert an error shows if trying to make it active
        with self.assertRaises(ValidationError):
            contact.write({"stage_id": self.stage_confirmed.id})

        # Request and validate partner
        contact.request_validation()
        contact.invalidate_recordset()
        contact.with_user(self.user_approver).validate_tier()
        contact.with_user(self.user_approver).write(
            {"stage_id": self.stage_confirmed.id}
        )
        self.assertEqual(contact.state, "confirmed")

        # Change company type to retrigger validation
        contact.write({"company_type": "person"})
        self.assertEqual(
            contact.state, "draft", "Change company type sets back to draft"
        )

    def test_no_validation_res_partner(self):
        """
        Case where new Contact does not require validation
        """
        Partner = self.env["res.partner"]
        contact_vals = {"name": "Company for test", "company_type": "person"}
        contact = Partner.with_user(self.user_employee).create(contact_vals)
        self.assertEqual(contact.state, "draft")
        # Can move to confirmed state without approval
        contact.write({"stage_id": self.stage_confirmed.id})
        self.assertEqual(contact.state, "confirmed")
