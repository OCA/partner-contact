# Copyright 2017-2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import exceptions
from odoo.tests import new_test_user

from odoo.addons.base.tests.common import BaseCommon


class TestPartnerDeduplicateAcl(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
        cls.user = new_test_user(
            cls.env,
            login="test_crm_deduplicate_acl",
            email="partner_deduplicate_acl@example.org",
            groups="base.group_partner_manager",
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
        # Although it should not be necessary, we apply sudo() because in some cases
        # the user may not have enough permissions to access some of the partner data;
        # for example website.visitor records
        self.wizard.sudo().action_merge()
