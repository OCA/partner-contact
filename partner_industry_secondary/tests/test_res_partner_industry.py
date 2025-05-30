# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# Copyright 2016 Tecnativa S.L. - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import UserError, ValidationError
from odoo.tests import common


class TestResPartnerIndustry(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.industry_model = cls.env["res.partner.industry"]
        cls.industry_main = cls.industry_model.create({"name": "Test"})
        cls.industry_child = cls.industry_model.create(
            {"name": "Test child", "parent_id": cls.industry_main.id}
        )
        cls.env.user.groups_id = [
            (
                4,
                cls.env.ref(
                    "partner_industry_secondary.group_use_partner_industry_for_person"
                ).id,
            )
        ]
        cls.partner = cls.env["res.partner"].create({"name": "Test partner"})

    def test_00_check_industries(self):
        """Verifies that a partner cannot have the same industry set as both
        main and secondary."""
        with self.assertRaises(ValidationError):
            self.env["res.partner"].create(
                {
                    "name": "Test",
                    "industry_id": self.industry_main.id,
                    "secondary_industry_ids": [(4, self.industry_main.id)],
                }
            )

    def test_01_check_copy(self):
        """Verifies that when duplicating an industry,
        a new name is automatically assigned."""
        industry_copy = self.industry_child.copy()
        self.assertEqual(industry_copy.name, "Test child 2")

    def test_02_check_uniq_name(self):
        """Ensures that two industries with the same name
        and parent cannot be created."""
        with self.assertRaises(ValidationError):
            self.industry_model.create({"name": "Test"})

    def test_03_check_recursion(self):
        """Checks that a recursive hierarchy among industries is not allowed."""
        with self.assertRaisesRegex(UserError, "Recursion Detected."):
            self.industry_main.parent_id = self.industry_child.id

    def test_04_name(self):
        """Verifies that the 'display_name' field correctly shows the hierarchy."""
        self.assertEqual(self.industry_child.display_name, "Test / Test child")

    def test_05_check_partner_industries(self):
        """Verifies that a partner cannot have the same industry set as both main
        and secondary."""
        main = self.industry_main
        both = self.industry_main | self.industry_child
        with self.assertRaises(ValidationError):
            self.partner.write(
                {"industry_id": main.id, "secondary_industry_ids": [(6, 0, both.ids)]}
            )

    def test_06_check_show_partner_industry_for_person(self):
        """Verifies that the system correctly computes whether to show industries
        for individuals, based on user group."""
        self.partner._compute_show_partner_industry_for_person()
        self.assertEqual(self.partner.show_partner_industry_for_person, True)
