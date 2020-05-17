# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# Copyright 2016 Tecnativa S.L. - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests import common


class TestResPartnerIndustry(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestResPartnerIndustry, cls).setUpClass()
        cls.industry_model = cls.env["res.partner.industry"]
        cls.industry_main = cls.industry_model.create({"name": "Test",})
        cls.industry_child = cls.industry_model.create(
            {"name": "Test child", "parent_id": cls.industry_main.id,}
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

    def test_check_recursion(self):
        with self.assertRaises(ValidationError):
            self.industry_main.parent_id = self.industry_child.id

    def test_name(self):
        self.assertEqual(
            self.industry_child.name_get()[0][1], "Test / Test child",
        )
