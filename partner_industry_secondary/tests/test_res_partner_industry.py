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
        with self.assertRaises(ValidationError):
            self.env["res.partner"].create(
                {
                    "name": "Test",
                    "industry_id": self.industry_main.id,
                    "secondary_industry_ids": [(4, self.industry_main.id)],
                }
            )

    def test_01_check_copy(self):
        industry_copy = self.industry_child.copy()
        self.assertEqual(industry_copy.name, "Test child 2")

    def test_02_check_uniq_name(self):
        with self.assertRaises(ValidationError):
            self.industry_model.create({"name": "Test"})

    def test_03_check_recursion(self):
        with self.assertRaises(UserError):
            self.industry_main.parent_id = self.industry_child.id

    def test_04_name(self):
        self.assertEqual(self.industry_child.display_name, "Test / Test child")

    def test_05_check_partner_industries(self):
        main = self.industry_main
        both = self.industry_main | self.industry_child
        with self.assertRaises(ValidationError):
            self.partner.write(
                {"industry_id": main.id, "secondary_industry_ids": [(6, 0, both.ids)]}
            )

    def test_06_check_show_partner_industry_for_person(self):
        self.partner._compute_show_partner_industry_for_person()
        self.assertEqual(self.partner.show_partner_industry_for_person, True)
