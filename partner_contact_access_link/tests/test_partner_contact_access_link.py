# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import TransactionCase


class TestPartnerContactAccessLink(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner_model = self.env["res.partner"]
        self.company = self.partner_model.create(
            {"name": "Test Company", "company_type": "company"}
        )
        self.contact = self.partner_model.create(
            {"name": "Test Contact", "type": "contact", "parent_id": self.company.id}
        )

    def test_partner_contact_access_link(self):
        res = self.contact.open_child_form()
        self.assertEqual(res["type"], "ir.actions.act_window")
        self.assertEqual(res["res_model"], "res.partner")
        self.assertEqual(res["res_id"], self.contact.id)
        self.assertEqual(res["view_mode"], "form")
        self.assertEqual(res["target"], "current")
