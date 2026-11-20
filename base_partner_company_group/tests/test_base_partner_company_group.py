# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.base.tests.common import BaseCommon


class TestBasePartnerCompanyGroup(BaseCommon):
    _test_user_groups = ("base.group_user", "base.group_partner_manager")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["res.partner"]
        cls.company = cls.partner_model.create(
            {
                "name": "Test Company",
                "is_company": True,
            }
        )
        cls.contact = cls.partner_model.create(
            {"name": "Test Contact", "type": "contact", "parent_id": cls.company.id}
        )

    def test_base_partner_company_group(self):
        self.company.write({"company_group_id": self.company.id})
        self.assertEqual(self.company.company_group_id, self.contact.company_group_id)
