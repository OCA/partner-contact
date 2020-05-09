# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import Form, common


class TestPortalPartnerSelctAll(common.TransactionCase):
    def setUp(self):
        super().setUp()

        Partner = self.env["res.partner"]
        self.partner1 = Partner.create({"name": "P1", "email": "p1@p1"})
        self.partner2 = Partner.create({"name": "P2", "email": "p2@p2"})
        self.partner3 = Partner.create({"name": "P3", "email": "p3@p3"})
        self.wizard_all = (
            self.env["portal.wizard"]
            .with_context({"active_ids": [self.partner1.id, self.partner2.id]})
            .create({})
        )
        self.wizard_default = (
            self.env["portal.wizard"]
            .with_context(
                {"active_ids": [self.partner1.id, self.partner2.id, self.partner3.id]}
            )
            .create({})
        )

    def test_portal_partner_select_all_wizard(self):
        # check selecting all
        wizard_all_form = Form(self.wizard_all)
        wizard_all_form.set_all_users = True
        w = wizard_all_form.save()
        w.action_apply()
        # partner should have user records with assigned portal group
        self.assertTrue(self.partner1.user_ids, "Partner should have user")
        self.assertTrue(self.partner2.user_ids, "Partner should have user")
        self.assertTrue(self.partner1.user_ids[0].has_group("base.group_portal"))
        self.assertTrue(self.partner2.user_ids[0].has_group("base.group_portal"))

        # checking toogle
        wizard_default_form = Form(self.wizard_default)
        wizard_default_form.set_all_users = True
        wizard_default_form.set_all_users = False
        w = wizard_default_form.save()
        w.action_apply()
        self.assertFalse(self.partner3.user_ids, "Partner shouldn't have a user")
