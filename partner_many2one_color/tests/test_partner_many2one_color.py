# Copyright 2026 glueckkanja AG
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json

from odoo import Command
from odoo.exceptions import AccessError
from odoo.tests.common import HttpCase, TransactionCase, new_test_user, tagged

COLOR_SPEC = {"many2one_color": {}, "many2one_color_message": {}}


@tagged("post_install", "-at_install")
class TestPartnerMany2oneColor(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = new_test_user(
            cls.env,
            login="partner_color_user",
            groups="base.group_user,base.group_partner_manager",
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Critical Partner",
                "own_many2one_color": "critical",
                "own_many2one_color_message": "Blocked",
            }
        )
        cls.plain_partner = cls.env["res.partner"].create({"name": "Plain Partner"})

    def test_partner_color_fields(self):
        """The partner exposes the color state and its message."""
        values = self.partner.with_user(self.user).web_read(COLOR_SPEC)
        self.assertEqual(
            values,
            [
                {
                    "id": self.partner.id,
                    "many2one_color": "critical",
                    "many2one_color_message": "Blocked",
                }
            ],
        )

    def test_color_models(self):
        """Contacts are reported to the web client as a color model."""
        models = self.env["many2one.color.mixin"]._get_many2one_color_models()
        self.assertIn("res.partner", models)

    def test_many2one_sub_fields(self):
        """The color state is returned as sub-field of a many2one value."""
        self.user.partner_id.write(
            {
                "own_many2one_color": "warning",
                "own_many2one_color_message": "Late payer",
            }
        )
        values = self.user.with_user(self.user).web_read(
            {"partner_id": {"fields": {"display_name": {}, **COLOR_SPEC}}}
        )
        self.assertEqual(
            values[0]["partner_id"],
            {
                "id": self.user.partner_id.id,
                "display_name": self.user.partner_id.display_name,
                "many2one_color": "warning",
                "many2one_color_message": "Late payer",
            },
        )

    def test_inaccessible_target_record(self):
        """Partners the user cannot read yield an empty color state, no error."""
        self.env["ir.rule"].create(
            {
                "name": "Hide the critical partner",
                "model_id": self.env.ref("base.model_res_partner").id,
                "domain_force": f"[('id', '!=', {self.partner.id})]",
                "groups": [Command.link(self.env.ref("base.group_user").id)],
            }
        )
        hidden = self.partner.with_user(self.user)
        with self.assertRaises(AccessError):
            hidden.web_read({"name": {}})
        partners = (self.plain_partner | self.partner).with_user(self.user)
        self.assertEqual(
            partners.web_read(COLOR_SPEC),
            [
                {
                    "id": self.plain_partner.id,
                    "many2one_color": False,
                    "many2one_color_message": False,
                },
                {
                    "id": self.partner.id,
                    "many2one_color": False,
                    "many2one_color_message": False,
                },
            ],
        )
        # The same through a many2one of a readable record
        child = self.env["res.partner"].create(
            {"name": "Child", "parent_id": self.partner.id, "type": "contact"}
        )
        values = child.with_user(self.user).web_read(
            {"parent_id": {"fields": {"display_name": {}, **COLOR_SPEC}}}
        )
        self.assertEqual(values[0]["parent_id"]["id"], self.partner.id)
        self.assertFalse(values[0]["parent_id"]["many2one_color"])
        # Other reads keep the regular access checks
        with self.assertRaises(AccessError):
            partners.web_read({"name": {}, **COLOR_SPEC})

    def _create_child(self, parent, **vals):
        return self.env["res.partner"].create(
            {"name": "Child", "parent_id": parent.id, "type": "contact", **vals}
        )

    def test_color_inherited_from_parent(self):
        """A contact without own color state takes over the parent's one."""
        child = self._create_child(self.partner)
        self.assertFalse(child.own_many2one_color)
        self.assertEqual(
            child.with_user(self.user).web_read(COLOR_SPEC),
            [
                {
                    "id": child.id,
                    "many2one_color": "critical",
                    "many2one_color_message": "Blocked",
                }
            ],
        )
        # The same as sub-field of a many2one value
        self.user.partner_id.parent_id = self.partner
        values = self.user.with_user(self.user).web_read(
            {"partner_id": {"fields": {"display_name": {}, **COLOR_SPEC}}}
        )
        self.assertEqual(values[0]["partner_id"]["many2one_color"], "critical")
        self.assertEqual(values[0]["partner_id"]["many2one_color_message"], "Blocked")

    def test_own_color_wins(self):
        """An own color state, even without message, overrides the parent's."""
        child = self._create_child(self.partner, own_many2one_color="warning")
        self.assertEqual(child.many2one_color, "warning")
        self.assertFalse(child.many2one_color_message)
        child.own_many2one_color_message = "Check first"
        self.assertEqual(child.many2one_color_message, "Check first")
        child.own_many2one_color = False
        self.assertEqual(child.many2one_color, "critical")
        self.assertEqual(child.many2one_color_message, "Blocked")

    def test_parent_change_propagates(self):
        """Changes of the parent or of the hierarchy update the children."""
        child = self._create_child(self.partner)
        grandchild = self._create_child(child)
        self.assertEqual(grandchild.many2one_color, "critical")
        self.assertEqual(grandchild.many2one_color_message, "Blocked")
        self.partner.write(
            {"own_many2one_color": "warning", "own_many2one_color_message": "Late"}
        )
        self.assertEqual(child.many2one_color, "warning")
        self.assertEqual(grandchild.many2one_color, "warning")
        self.assertEqual(grandchild.many2one_color_message, "Late")
        child.own_many2one_color = "critical"
        self.assertEqual(grandchild.many2one_color, "critical")
        self.assertFalse(grandchild.many2one_color_message)
        grandchild.parent_id = self.plain_partner
        self.assertFalse(grandchild.many2one_color)
        self.assertFalse(grandchild.many2one_color_message)
        self.partner.own_many2one_color = False
        child.own_many2one_color = False
        self.assertFalse(self.partner.many2one_color)
        self.assertFalse(child.many2one_color)
        self.assertFalse(child.many2one_color_message)

    def test_inaccessible_parent(self):
        """The color state is inherited from a parent the user cannot read."""
        self.env["ir.rule"].create(
            {
                "name": "Hide the critical partner",
                "model_id": self.env.ref("base.model_res_partner").id,
                "domain_force": f"[('id', '!=', {self.partner.id})]",
                "groups": [Command.link(self.env.ref("base.group_user").id)],
            }
        )
        child = self._create_child(self.partner).with_user(self.user)
        child.invalidate_recordset()
        self.assertEqual(
            child.web_read(COLOR_SPEC),
            [
                {
                    "id": child.id,
                    "many2one_color": "critical",
                    "many2one_color_message": "Blocked",
                }
            ],
        )
        # Writing the child recomputes the state as that user
        child.write({"name": "Renamed Child", "parent_id": self.partner.id})
        child.invalidate_recordset()
        self.assertEqual(child.many2one_color, "critical")


@tagged("post_install", "-at_install")
class TestSessionInfo(HttpCase):
    def test_session_info_lists_partner(self):
        """The web client is told that contacts provide a color state."""
        self.authenticate("admin", "admin")
        response = self.url_open(
            "/web/session/get_session_info",
            data=json.dumps({"jsonrpc": "2.0", "method": "call", "params": {}}),
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        session_info = response.json()["result"]
        self.assertIn("res.partner", session_info["many2one_color_models"])
