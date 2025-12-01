# Copyright 2026 Therp BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestPartnerMultiRelationArchivePropagate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(su=True)
        Partners = cls.env["res.partner"]
        RelationType = cls.env["res.partner.relation.type"]
        Relation = cls.env["res.partner.relation"]
        # Organisation and two related partners
        cls.org = Partners.create({"name": "Org", "is_company": True})
        cls.rel1 = Partners.create({"name": "Rel1"})
        cls.rel2 = Partners.create({"name": "Rel2"})
        # Relation type with propagation enabled
        cls.rel_type = RelationType.create(
            {
                "name": "Org -> Rel",
                "name_inverse": "Rel -> Org",
                "propagate_archive": True,
            }
        )
        # Create relations from org to rel1 and rel2
        Relation.create(
            {
                "type_id": cls.rel_type.id,
                "left_partner_id": cls.org.id,
                "right_partner_id": cls.rel1.id,
            }
        )
        Relation.create(
            {
                "type_id": cls.rel_type.id,
                "left_partner_id": cls.org.id,
                "right_partner_id": cls.rel2.id,
            }
        )

    def setUp(self):
        super().setUp()
        # Restore all partners to a clean active state before each test so that
        # user records created in one test cannot affect another.
        (self.org | self.rel1 | self.rel2).write(
            {"active": True, "propagated_from_id": False}
        )

    def _create_active_user_for_partner(self, partner, login):
        """Create an active user linked to a partner."""
        return (
            self.env["res.users"]
            .sudo()
            .create(
                {
                    "name": partner.name,
                    "login": login,
                    "partner_id": partner.id,
                    "email": "amail@mail.com",
                }
            )
        )

    def test_archive_org_archives_related_external(self):
        """External archive (force_outside_ui) propagates to related partners.

        rel1 has no active user -> archived and flagged.
        rel2 has an active user -> skipped, warning posted on org.
        """
        icp = self.env["ir.config_parameter"].sudo()
        icp.set_param("partner_archive_propagate.force_outside_ui", "1")
        self.addCleanup(
            icp.set_param, "partner_archive_propagate.force_outside_ui", "0"
        )
        user = self._create_active_user_for_partner(self.rel2, "rel2_user_ext")
        self.addCleanup(user.unlink)
        self.org.write({"active": False})
        self.assertFalse(self.org.active)
        self.rel1.invalidate_recordset()
        self.assertFalse(self.rel1.active)
        self.assertEqual(self.rel1.propagated_from_id, self.org)
        self.rel2.invalidate_recordset()
        self.assertTrue(self.rel2.active)
        self.assertFalse(bool(self.rel2.propagated_from_id))
        skipped_msgs = self.org.message_ids.filtered(
            lambda m: m.body
            and "Skipped archiving the following contacts" in m.body
            and self.rel2.name in m.body
        )
        self.assertTrue(skipped_msgs)

    def test_unarchive_org_restores_related(self):
        """Unarchiving restores only related partners flagged as propagated from org."""
        self.org.write({"active": False})
        self.rel1.write({"active": False, "propagated_from_id": self.org.id})
        self.rel2.write({"active": False, "propagated_from_id": False})
        self.org.write({"active": True})
        self.assertTrue(self.org.active)
        self.rel1.invalidate_recordset()
        self.assertTrue(self.rel1.active)
        self.assertFalse(bool(self.rel1.propagated_from_id))
        self.rel2.invalidate_recordset()
        self.assertFalse(self.rel2.active)
        self.assertFalse(bool(self.rel2.propagated_from_id))

    def test_non_company_does_not_propagate(self):
        """Archiving a non-company must not propagate via relations."""
        person = self.env["res.partner"].create({"name": "Person", "is_company": False})
        rel_type = self.env["res.partner.relation.type"].create(
            {
                "name": "Person -> Rel1",
                "name_inverse": "Rel1 -> Person",
                "propagate_archive": True,
            }
        )
        self.env["res.partner.relation"].create(
            {
                "type_id": rel_type.id,
                "left_partner_id": person.id,
                "right_partner_id": self.rel1.id,
            }
        )
        icp = self.env["ir.config_parameter"].sudo()
        icp.set_param("partner_archive_propagate.force_outside_ui", "1")
        self.addCleanup(
            icp.set_param, "partner_archive_propagate.force_outside_ui", "0"
        )
        person.write({"active": False})
        self.assertFalse(person.active)
        self.rel1.invalidate_recordset()
        self.assertTrue(self.rel1.active)
        self.assertFalse(bool(self.rel1.propagated_from_id))

    def test_archive_propagate_wizard_archives_related(self):
        """Wizard UI path: _archive_propagate_wizard archives related partners.

        When action_confirm writes active=False with partner_archive_propagate_ui
        context, _archive_propagate_wizard is called. The glue module's override
        must invoke _archive_multi_relation so related partners are archived
        alongside non-contact hierarchy descendants.
        """
        self.org.with_context(partner_archive_propagate_ui=True).write(
            {"active": False}
        )
        self.assertFalse(self.org.active)
        self.rel1.invalidate_recordset()
        self.assertFalse(self.rel1.active)
        self.assertEqual(self.rel1.propagated_from_id, self.org)
        self.rel2.invalidate_recordset()
        self.assertFalse(self.rel2.active)
        self.assertEqual(self.rel2.propagated_from_id, self.org)

    def test_archive_propagate_wizard_skips_related_with_active_user(self):
        """Wizard UI path: related partner with an active user is skipped
        and a notification is posted on the organisation."""
        user = self._create_active_user_for_partner(self.rel2, "rel2_user_wiz")
        self.addCleanup(user.unlink)
        before_msgs = len(self.org.message_ids)
        self.org.with_context(partner_archive_propagate_ui=True).write(
            {"active": False}
        )

        self.assertFalse(self.org.active)
        self.rel1.invalidate_recordset()
        self.assertFalse(self.rel1.active)
        self.assertEqual(self.rel1.propagated_from_id, self.org)
        self.rel2.invalidate_recordset()
        self.assertTrue(self.rel2.active)
        self.assertFalse(bool(self.rel2.propagated_from_id))
        self.assertGreater(len(self.org.message_ids), before_msgs)
        latest = self.org.message_ids.sorted("id")[-1]
        self.assertIn(self.rel2.name, latest.body)

    def test_show_wizard_button_for_company_with_relations(self):
        """show_prop_wizard_button is True for a company with propagating
        relations even when it has no hierarchical child_ids."""
        self.assertFalse(bool(self.org.child_ids))
        self.org.invalidate_recordset()
        self.assertTrue(self.org.show_prop_wizard_button)

    def test_action_archive_with_contacts_opens_wizard_for_relations(self):
        """action_archive_with_contacts opens the wizard when the only contacts
        are via propagating relation types (no hierarchical children)."""
        self.assertFalse(bool(self.org.child_ids))
        self.rel1.write({"type": "contact"})
        self.rel2.write({"type": "contact"})
        action = self.org.action_archive_with_contacts()
        self.assertIsInstance(action, dict)
        self.assertEqual(
            action.get("res_model"), "res.partner.archive.propagate.wizard"
        )
        self.assertEqual(action.get("target"), "new")
        wiz = self.env["res.partner.archive.propagate.wizard"].browse(action["res_id"])
        line_partners = wiz.line_ids.mapped("partner_id")
        self.assertIn(self.rel1, line_partners)
        self.assertIn(self.rel2, line_partners)

    def test_action_archive_with_contacts_excludes_user_linked_from_wizard(self):
        """Related partners linked to active users must not appear in wizard
        lines; a notification must be posted on the organisation instead."""
        self.rel1.write({"type": "contact"})
        self.rel2.write({"type": "contact"})
        user = self._create_active_user_for_partner(self.rel2, "rel2_user_wiz2")
        self.addCleanup(user.unlink)
        before_msgs = len(self.org.message_ids)
        action = self.org.action_archive_with_contacts()
        wiz = self.env["res.partner.archive.propagate.wizard"].browse(action["res_id"])
        line_partners = wiz.line_ids.mapped("partner_id")
        self.assertIn(self.rel1, line_partners)
        self.assertNotIn(self.rel2, line_partners)
        self.assertGreater(len(self.org.message_ids), before_msgs)

    def test_get_archive_propagation_candidates_union(self):
        """_get_archive_propagation_candidates returns the union of hierarchy
        descendants and propagating-relation partners, excluding self."""
        self.rel1.write({"type": "contact"})
        self.rel2.write({"type": "contact"})
        child = self.env["res.partner"].create(
            {"name": "Child Contact", "parent_id": self.org.id, "type": "contact"}
        )

        descendants = self.org._get_descendants()
        self.assertIn(child, descendants)
        self.assertNotIn(self.rel1, descendants)
        self.assertNotIn(self.rel2, descendants)

        candidates = self.org._get_archive_propagation_candidates()
        self.assertIn(child, candidates)
        self.assertIn(self.rel1, candidates)
        self.assertIn(self.rel2, candidates)
        self.assertNotIn(self.org, candidates)

    def test_show_wizard_button_false_when_no_propagating_relations(self):
        """_compute_show_prop_wizard_button: company with no propagating-archive
        relations falls back to super() logic (child_ids only).
        A company with neither child_ids nor propagating relations must have
        show_prop_wizard_button=False."""
        org2 = self.env["res.partner"].create(
            {"name": "Org2 no relations", "is_company": True}
        )
        org2.invalidate_recordset()
        self.assertFalse(org2.show_prop_wizard_button)

    def test_get_related_partners_self_as_right_partner(self):
        """_get_related_partners_for_archive_propagation: when self is the
        RIGHT partner of a relation, the LEFT partner must be returned."""
        other_org = self.env["res.partner"].create(
            {"name": "Other Org", "is_company": True}
        )
        # rel1 is on the RIGHT side of a propagating relation pointing to other_org
        self.env["res.partner.relation"].create(
            {
                "type_id": self.rel_type.id,
                "left_partner_id": other_org.id,
                "right_partner_id": self.rel1.id,
            }
        )
        related = self.rel1._get_related_partners_for_archive_propagation()
        # other_org must be returned (self was on the right, so left is "other")
        self.assertIn(other_org, related)

    def test_archive_multi_relation_no_related_skips_gracefully(self):
        """_archive_multi_relation: company with no active related partners
        must not raise and must leave everything untouched."""
        org3 = self.env["res.partner"].create(
            {"name": "Org3 no relations", "is_company": True}
        )
        # Should not raise; nothing to archive
        org3._archive_multi_relation()
        self.assertTrue(org3.active)
