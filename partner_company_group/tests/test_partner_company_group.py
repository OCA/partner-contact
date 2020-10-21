# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestPartnerCompanyGroup(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner_model = self.env["res.partner"]
        self.company = self.partner_model.create(
            {"name": "Test Company", "company_type": "company"}
        )
        self.contact = self.partner_model.create(
            {"name": "Test Contact", "type": "contact", "parent_id": self.company.id}
        )

    def test_partner_company_group(self):
        self.company.write({"company_group_id": self.company.id})
        self.assertEqual(self.company.company_group_id, self.contact.company_group_id)
