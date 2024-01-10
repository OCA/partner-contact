# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import TransactionCase


class TestPartnerContactAccessLink(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Remove this variable in v16 and put instead:
        # from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT
        DISABLED_MAIL_CONTEXT = {
            "tracking_disable": True,
            "mail_create_nolog": True,
            "mail_create_nosubscribe": True,
            "mail_notrack": True,
            "no_reset_password": True,
        }
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        cls.partner_model = cls.env["res.partner"]
        cls.company = cls.partner_model.create(
            {"name": "Test Company", "company_type": "company"}
        )
        cls.contact = cls.partner_model.create(
            {"name": "Test Contact", "type": "contact", "parent_id": cls.company.id}
        )

    def test_partner_contact_access_link(self):
        res = self.contact.open_child_form()
        self.assertEqual(res["type"], "ir.actions.act_window")
        self.assertEqual(res["res_model"], "res.partner")
        self.assertEqual(res["res_id"], self.contact.id)
        self.assertEqual(res["view_mode"], "form")
        self.assertEqual(res["view_type"], "form")
        self.assertEqual(res["target"], "current")
