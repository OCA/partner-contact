# Copyright 2021 Patrick Wilson <pwilson@opensourceintegrators.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.exceptions import ValidationError
from odoo.tests import tagged

from odoo.addons.base.tests.common import BaseCommon, new_test_user


@tagged("-at_install", "post_install")
class TestPartnerTierValidation(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create users
        cls.user_employee = new_test_user(
            env=cls.env,
            login="empl1",
            groups="base.group_user,base.group_partner_manager",
        )
        cls.user_approver = new_test_user(
            env=cls.env,
            login="aprov1",
            groups="base.group_user,base.group_partner_manager,base.group_no_one",
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
        partner_obj = self.env["res.partner"]
        contact_vals = {"name": "Company for test", "company_type": "company"}
        contact = partner_obj.with_user(self.user_employee).create(contact_vals)
        self.assertEqual(contact.stage_state, "draft")

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
        self.assertEqual(contact.stage_state, "confirmed")

        # Change company type to retrigger validation
        contact.write({"company_type": "person"})
        self.assertEqual(
            contact.stage_state, "draft", "Change company type sets back to draft"
        )

    def test_no_validation_res_partner(self):
        """
        Case where new Contact does not require validation
        """
        partner_obj = self.env["res.partner"]
        contact_vals = {"name": "Company for test", "company_type": "person"}
        contact = partner_obj.with_user(self.user_employee).create(contact_vals)
        self.assertEqual(contact.stage_state, "draft")
        # Can move to confirmed state without approval
        contact.write({"stage_id": self.stage_confirmed.id})
        self.assertEqual(contact.stage_state, "confirmed")

    def test_validation_res_partner_restarted(self):
        """
        Case where new Contact validation is removed upon restart because of
        stage changed to draft
        """
        Partner = self.env["res.partner"]
        contact_vals = {"name": "Company for test", "company_type": "company"}
        contact = Partner.with_user(self.user_employee).create(contact_vals)
        self.assertEqual(contact.stage_state, "draft")
        self.assertEqual(contact.validation_status, "no")
        self.assertFalse(contact.review_ids.status)
        # Request and validate partner
        contact.request_validation()
        contact.invalidate_recordset()
        self.assertEqual(contact.validation_status, "pending")
        self.assertEqual(contact.review_ids.status, "pending")
        contact.with_user(self.user_approver).validate_tier()
        self.assertEqual(contact.validation_status, "validated")
        self.assertEqual(contact.review_ids.status, "approved")
        # change stage to confirmed
        contact.with_user(self.user_approver).write(
            {"stage_id": self.stage_confirmed.id}
        )
        self.assertEqual(contact.stage_state, "confirmed")
        # validation didn't change
        self.assertEqual(contact.validation_status, "validated")
        self.assertEqual(contact.review_ids.status, "approved")
        # change stage to draft
        contact.with_user(self.user_approver).write({"stage_id": self.stage_draft.id})
        self.assertEqual(contact.stage_state, "draft")
        # validation removed by restart
        self.assertEqual(contact.validation_status, "no")
        self.assertFalse(contact.review_ids.status)

    def test_partner_tier_revalidation_fields(self):
        fields_set = self.env["res.partner"]._partner_tier_revalidation_fields({})
        self.assertIn("company_type", fields_set)
        self.assertIn("parent_id", fields_set)
