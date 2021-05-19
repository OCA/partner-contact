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
                "email": "test@examlple.com",
            }
        )

        # Create tier definitions:
        cls.tier_def_obj = cls.env["tier.definition"]
        cls.tier_def_obj.create(
            {
                "model_id": cls.partner_model.id,
                "review_type": "individual",
                "reviewer_id": cls.test_user_1.id,
                "definition_domain": "['&',('is_company','=',True),'|', \
                ('active','=',True),('active','=',False)]",
            }
        )

    def test_tier_validation_model_name(self):
        self.assertIn(
            "res.partner", self.tier_def_obj._get_tier_validation_model_names()
        )

    def test_validation_res_partner(self):
        company = self.env["res.partner"].create(
            {"name": "Company for test", "company_type": "company"}
        )
        # Since company need validation, it should be inactive
        self.assertEqual(company.active, False)

        # Assert an error shows if trying to make it active
        with self.assertRaises(ValidationError):
            company.write({"state": "confirmed"})

        # Request and validate partner
        company.request_validation()
        company.with_user(self.test_user_1).validate_tier()
        company.with_user(self.test_user_1).write({"state": "confirmed"})
        self.assertEqual(company.state, "confirmed")

        # Change company type to retrigger validation
        company.write({"company_type": "person", "is_company": False})
        self.assertEqual(company.state, "draft")

        # Test partner creation that doesn't need validation
        customer = self.env["res.partner"].create({"name": "Partner for test"})
        self.assertEqual(customer.active, True)
