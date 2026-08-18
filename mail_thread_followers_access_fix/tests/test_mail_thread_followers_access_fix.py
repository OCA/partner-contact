# Copyright 2026 Canarias Conectada
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import new_test_user, tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestMailThreadFollowersAccessFix(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.merchant = new_test_user(
            cls.env,
            login="followers_fix_merchant",
            groups="base.group_user,base.group_partner_manager",
        )
        cls.visible_colleague = new_test_user(
            cls.env, login="followers_fix_visible", groups="base.group_user"
        )
        cls.hidden_colleague = new_test_user(
            cls.env, login="followers_fix_hidden", groups="base.group_user"
        )
        # Simulate a partner-visibility restriction (independent of any of
        # this repo's other modules): hide hidden_colleague from everyone,
        # to reproduce the crash this module fixes.
        cls.env["ir.rule"].sudo().create(
            {
                "name": "Test: hide one partner",
                "model_id": cls.env.ref("base.model_res_partner").id,
                "domain_force": str([("id", "!=", cls.hidden_colleague.partner_id.id)]),
            }
        )
        cls.document = cls.env["res.partner"].create({"name": "Followers Fix Test Doc"})
        cls.document.sudo().message_subscribe(
            [cls.visible_colleague.partner_id.id, cls.hidden_colleague.partner_id.id]
        )

    def test_hidden_follower_does_not_crash_read(self):
        doc = self.document.with_user(self.merchant)
        doc.invalidate_recordset()
        followers = doc.message_partner_ids  # must not raise
        self.assertIn(self.visible_colleague.partner_id, followers)
        self.assertNotIn(self.hidden_colleague.partner_id, followers)

    def test_no_restriction_shows_all_followers(self):
        # With the (test-only) visibility rule out of the way, the fix
        # still shows every follower -- it only omits what a genuine
        # restriction actually blocks, it does not drop followers on its
        # own.
        rule = (
            self.env["ir.rule"].sudo().search([("name", "=", "Test: hide one partner")])
        )
        rule.active = False
        try:
            doc = self.document.with_user(self.merchant)
            doc.invalidate_recordset()
            followers = doc.message_partner_ids
            self.assertIn(self.visible_colleague.partner_id, followers)
            self.assertIn(self.hidden_colleague.partner_id, followers)
        finally:
            rule.active = True
