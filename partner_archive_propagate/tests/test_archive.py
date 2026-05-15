# Copyright 2025 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class TestPartnerArchivePropagate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # just sudo everywhere
        cls.env = cls.env(su=True)
        Partners = cls.env["res.partner"]
        # Parent: A (company)
        # Children: B(contact), C(delivery), D(invoice), E(child of B, contact)
        cls.A = Partners.create({"name": "A", "is_company": True})
        cls.B = Partners.create({"name": "B", "parent_id": cls.A.id, "type": "contact"})
        cls.C = Partners.create(
            {"name": "C", "parent_id": cls.A.id, "type": "delivery"}
        )
        cls.D = Partners.create({"name": "D", "parent_id": cls.A.id, "type": "invoice"})
        cls.E = Partners.create({"name": "E", "parent_id": cls.B.id, "type": "contact"})

    def _create_active_user_for_partner(self, partner):
        """Create an active user linked to given partner to test unarchivable situations"""
        return (
            self.env["res.users"]
            .sudo()
            .create(
                {
                    "name": partner.name,
                    "login": "test@test.test",
                    "partner_id": partner.id,
                    "email": "test@tset.org",
                }
            )
        )

    def test_archive_non_contact_type(self):
        """If there are no type contact descendants,
        the wizard should not open and archiving should proceed immediately.
        """
        # turn B/E into non-contact types so only non-contacts exist
        self.B.write({"type": "delivery"})
        self.E.write({"type": "invoice"})
        # launch wizard from company, but no children are type contact
        res = self.A.action_archive_with_contacts()
        self.assertTrue(res in (True, None))
        self.assertFalse(self.A.active)
        # All descendants of non-contact type should be archived and flagged
        for p in (self.B, self.C, self.D, self.E):
            self.assertFalse(p.active)
            self.assertEqual(
                p.propagated_from_id,
                self.A,
                "Descendant should be archived with propagated_from_id=A",
            )
        # Revert types for other tests
        self.B.write({"type": "contact"})
        self.E.write({"type": "contact"})
        # Unarchive company, flagged descendants must be restored
        self.A.write({"active": True})
        for p in (self.B, self.C, self.D, self.E):
            self.assertTrue(p.active)
            self.assertFalse(
                bool(p.propagated_from_id),
                "propagated_from_id should be cleared on unarchive",
            )

    def test_archive_contact_types_skip_active_user(self):
        """Wizard opens for type contact children.
        Children linked to active users are skipped.
        """
        # Ensure we have contact descendants
        self.B.write({"type": "contact"})
        self.E.write({"type": "contact"})
        # Block B by linking an active user
        self._create_active_user_for_partner(self.B)
        action = self.A.action_archive_with_contacts()
        self.assertEqual(
            action.get("res_model"), "res.partner.archive.propagate.wizard"
        )
        # Load wizard and confirm
        Wiz = (
            self.env["res.partner.archive.propagate.wizard"]
            .sudo()
            .browse(action["res_id"])
        )
        # Only archivable contacts should be in the lines
        line_partners = Wiz.line_ids.mapped("partner_id")
        self.assertIn(self.E, line_partners)
        self.assertNotIn(self.B, line_partners)
        result = Wiz.action_confirm()
        #  The window closes, silently
        self.assertEqual(result, {"type": "ir.actions.act_window_close"})
        # Parent should be inactive
        self.assertFalse(self.A.active)
        # B is linked to active user, partner remains active and unflagged
        self.assertTrue(self.B.active)
        self.assertFalse(bool(self.B.propagated_from_id))
        # E should be archived and flagged from A
        self.assertFalse(self.E.active)
        self.assertEqual(self.E.propagated_from_id, self.A)
        # C and D (type is not contact) archived silently and flagged from A
        for p in (self.C, self.D):
            self.assertFalse(p.active)
            self.assertEqual(p.propagated_from_id, self.A)
        # Unarchive parent: flagged ones E/C/D should become active, B stays active anyway
        self.A.write({"active": True})
        for p in (self.E, self.C, self.D):
            self.assertTrue(p.active)
            self.assertFalse(bool(p.propagated_from_id))
        self.assertTrue(self.B.active)
        self.assertFalse(bool(self.B.propagated_from_id))

    def test_archive_no_wizard_force_setting_propagates(self):
        """When force_outside_ui is enabled,
        all operations except wizard stuff can archive children
        """
        icp = self.env["ir.config_parameter"].sudo()
        icp.set_param("partner_archive_propagate.force_outside_ui", "1")
        # Ensure clean active state
        for p in (self.A, self.B, self.C, self.D, self.E):
            p.write({"active": True, "propagated_from_id": False})
        # Archive without UI
        self.A.write({"active": False})
        self.assertFalse(self.A.active)
        for p in (self.B, self.C, self.D, self.E):
            self.assertFalse(p.active)
            self.assertEqual(p.propagated_from_id, self.A)
        # Unarchive parent restores flagged children
        self.A.write({"active": True})
        for p in (self.B, self.C, self.D, self.E):
            self.assertTrue(p.active)
            self.assertFalse(bool(p.propagated_from_id))
        # Reset the setting
        icp.set_param("partner_archive_propagate.force_outside_ui", "0")

    def test_manual_archive_does_not_toggle_flag(self):
        """Archiving a partner manually should NOT toggle propagated_from_id on that record."""
        # Ensure clean
        self.B.write({"active": True, "propagated_from_id": False})
        # Manual archive of B, force_outside_ui is off
        self.env["ir.config_parameter"].sudo().set_param(
            "partner_archive_propagate.force_outside_ui", "0"
        )
        self.B.write({"active": False})
        self.assertFalse(self.B.active)
        self.assertFalse(bool(self.B.propagated_from_id))
        # Manual unarchive keeps it False
        self.B.write({"active": True})
        self.assertTrue(self.B.active)
        self.assertFalse(bool(self.B.propagated_from_id))

    def test_notify_skipped_partners_posts_message(self):
        """_notify_skipped_partners should post a message listing skipped partners."""
        before = len(self.A.message_ids)
        # Calling with empty recordset should do exactly nothing
        empty_partners = self.env["res.partner"]
        self.A._notify_skipped_partners(empty_partners)
        self.assertEqual(
            len(self.A.message_ids),
            before,
        )
        # Calling with some skipped partners should create exactly one message
        skipped = self.B | self.E
        self.A._notify_skipped_partners(skipped)
        self.assertEqual(
            len(self.A.message_ids),
            before + 1,
        )
        msg = self.A.message_ids.sorted("id")[-1]
        self.assertIn(
            "Skipped archiving the following contacts",
            msg.body,
        )
        self.assertIn(self.B.name, msg.body)
        self.assertIn(self.E.name, msg.body)

    def test_wizard_confirm_mixed_notification(self):
        """action_confirm should use split_archivable_unarchivable_user and
        return a display_notification when there are unarchivable partners.
        """
        self.B.write({"type": "contact", "active": True, "propagated_from_id": False})
        self.E.write({"type": "contact", "active": True, "propagated_from_id": False})
        self._create_active_user_for_partner(self.B)
        Wiz = (
            self.env["res.partner.archive.propagate.wizard"]
            .sudo()
            .create(
                {
                    "partner_id": self.A.id,
                    "line_ids": [
                        (0, 0, {"partner_id": self.B.id}),
                        (0, 0, {"partner_id": self.E.id}),
                    ],
                }
            )
        )

        result = Wiz.action_confirm()
        # Parent should be archived by the wizard
        self.assertFalse(self.A.active)
        # E must be archived and flagged from A
        self.assertFalse(self.E.active)
        self.assertEqual(self.E.propagated_from_id, self.A)
        # B must stay active and unflagged
        self.assertTrue(self.B.active)
        self.assertFalse(bool(self.B.propagated_from_id))
        # Result must be a display_notification about skipped contacts
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("type"), "ir.actions.client")
        self.assertEqual(result.get("tag"), "display_notification")
        params = result.get("params", {})
        self.assertIn("message", params)
        self.assertIn("Skipped contacts linked to active users", params["message"])
        # for partner B
        self.assertIn(self.B.name, params["message"])

    def test_wizard_deleted_line_not_archived(self):
        self.B.write({"type": "contact", "active": True, "propagated_from_id": False})
        self.E.write({"type": "contact", "active": True, "propagated_from_id": False})
        self.A.write({"active": True})
        # Simulate user removing B from the list: only E remains in line_ids.
        Wiz = (
            self.env["res.partner.archive.propagate.wizard"]
            .sudo()
            .create(
                {
                    "partner_id": self.A.id,
                    "line_ids": [(0, 0, {"partner_id": self.E.id})],
                }
            )
        )
        result = Wiz.action_confirm()
        self.assertEqual(result, {"type": "ir.actions.act_window_close"})
        # Organisation must be archived
        self.assertFalse(self.A.active)
        # E was in the list and must be archived
        self.assertFalse(self.E.active)
        self.assertEqual(self.E.propagated_from_id, self.A)
        # B was removed from the list and must remain as it was
        self.assertTrue(self.B.active)
        self.assertFalse(bool(self.B.propagated_from_id))
