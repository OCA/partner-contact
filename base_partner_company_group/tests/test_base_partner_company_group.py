# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestBasePartnerCompanyGroup(TransactionCase):
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

    def test_base_partner_company_group(self):
        self.company.write({"company_group_id": self.company.id})
        self.assertEqual(self.company.company_group_id, self.contact.company_group_id)
