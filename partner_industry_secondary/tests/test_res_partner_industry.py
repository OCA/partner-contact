# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# Copyright 2016 Tecnativa S.L. - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import UserError, ValidationError
from odoo.tests import common


class TestResPartnerIndustry(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestResPartnerIndustry, cls).setUpClass()
        cls.industry_model = cls.env["res.partner.industry"]
        cls.industry_main = cls.industry_model.create({"name": "Test"})
        cls.industry_child = cls.industry_model.create(
            {"name": "Test child", "parent_id": cls.industry_main.id}
        )

    def test_check_industries(self):
        with self.assertRaises(ValidationError):
            self.env["res.partner"].create(
                {
                    "name": "Test",
                    "industry_id": self.industry_main.id,
                    "secondary_industry_ids": [(4, self.industry_main.id)],
                }
            )

    def test_check_copy(self):
        industry_copy = self.industry_child.copy()
        self.assertEqual(industry_copy.name, "Test child 2")

    def test_check_uniq_name(self):
        with self.assertRaises(ValidationError):
            self.industry_model.create({"name": "Test"})

    def test_check_recursion(self):
        with self.assertRaises(UserError):
            self.industry_main.parent_id = self.industry_child.id

    def test_name(self):
        self.assertEqual(self.industry_child.display_name, "Test / Test child")
