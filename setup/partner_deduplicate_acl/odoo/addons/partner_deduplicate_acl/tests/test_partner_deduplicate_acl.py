# Copyright 2017-2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import exceptions
from odoo.tests import common


class TestPartnerDeduplicateAcl(common.TransactionCase):
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
        cls.partner_1 = cls.env["res.partner"].create(
            {
                "name": "Partner 1",
                "email": "partner1@example.org",
                "is_company": True,
                "parent_id": False,
            }
        )
        cls.partner_2 = cls.partner_1.copy()
        cls.partner_2.write({"name": "Partner 1", "email": "partner2@example.org"})
        cls.user = cls.env["res.users"].create(
            {
                "login": "test_crm_deduplicate_acl",
                "name": "test_crm_deduplicate_acl",
                "email": "partner_deduplicate_acl@example.org",
                "groups_id": [
                    (4, cls.env.ref("base.group_user").id),
                    (4, cls.env.ref("base.group_partner_manager").id),
                ],
            }
        )
        cls.wizard = (
            cls.env["base.partner.merge.automatic.wizard"]
            .with_user(cls.user)
            .create({"group_by_name": True})
        )

    def test_same_email_restriction(self):
        self.wizard.action_start_manual_process()
        with self.assertRaises(exceptions.UserError):
            self.wizard.action_merge()
        self.user.groups_id = [
            (4, self.env.ref("partner_deduplicate_acl.group_unrestricted").id)
        ]
        # Now there shouldn't be error
        self.wizard.action_merge()
