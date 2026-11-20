# Copyright 2026 Open Source Integrators
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestOwnerCompanySync(TransactionCase):
    """Contacts below a parent contact follow the parent's owner company."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_a = cls.env.company
        cls.company_b = cls.env["res.company"].create({"name": "Owner Sync B"})
        cls.parent_a = cls.env["res.partner"].create(
            {
                "name": "Owner Sync Parent A",
                "owner_company_id": cls.company_a.id,
            }
        )
        cls.parent_b = cls.env["res.partner"].create(
            {
                "name": "Owner Sync Parent B",
                "owner_company_id": cls.company_b.id,
            }
        )

    def test_children_inherit_owner_on_creation(self):
        """Contacts created under a parent adopt the parent's owner company,
        even company contacts or contacts asking for another owner."""
        children = self.env["res.partner"].create(
            [
                {"name": "Owner Sync Child", "parent_id": self.parent_a.id},
                {
                    "name": "Owner Sync Child Conflicting",
                    "parent_id": self.parent_a.id,
                    "owner_company_id": self.company_b.id,
                },
                {
                    "name": "Owner Sync Child Company",
                    "parent_id": self.parent_a.id,
                    "is_company": True,
                },
            ]
        )
        self.assertEqual(children.mapped("owner_company_id"), self.company_a)
        for child in children:
            self.assertEqual(child.owner_company_id, self.company_a)

    def test_owner_changes_reach_archived_descendants(self):
        """Updating a parent's owner company propagates through the whole
        descendant tree, archived records included."""
        child = self.env["res.partner"].create(
            {
                "name": "Owner Sync Child",
                "parent_id": self.parent_a.id,
                "owner_company_id": self.company_a.id,
            }
        )
        grandchild = self.env["res.partner"].create(
            {
                "name": "Owner Sync Grandchild",
                "parent_id": child.id,
                "owner_company_id": self.company_a.id,
            }
        )
        grandchild.write({"active": False})
        self.assertEqual(child.owner_company_id, self.company_a)
        self.assertEqual(grandchild.owner_company_id, self.company_a)
        self.parent_a.write({"owner_company_id": self.company_b.id})
        self.assertEqual(child.owner_company_id, self.company_b)
        self.assertEqual(grandchild.owner_company_id, self.company_b)
        self.parent_a.write({"owner_company_id": False})
        self.assertFalse(child.owner_company_id)
        self.assertFalse(grandchild.owner_company_id)
        self.assertEqual(self.parent_b.owner_company_id, self.company_b)

    def test_reparenting_and_detaching(self):
        """Reparenting moves a contact's whole subtree to the new parent's
        owner company; detaching keeps the last inherited owner and turns
        the contact back into an independent root."""
        child = self.env["res.partner"].create(
            {"name": "Owner Sync Child", "parent_id": self.parent_a.id}
        )
        grandchild = self.env["res.partner"].create(
            {"name": "Owner Sync Grandchild", "parent_id": child.id}
        )
        child.write(
            {
                "parent_id": self.parent_b.id,
                "owner_company_id": self.company_a.id,
            }
        )
        self.assertEqual(child.owner_company_id, self.company_b)
        self.assertEqual(grandchild.owner_company_id, self.company_b)
        child.write({"parent_id": False})
        self.assertEqual(child.owner_company_id, self.company_b)
        self.assertEqual(grandchild.owner_company_id, self.company_b)
        child.write({"owner_company_id": self.company_a.id})
        self.assertEqual(child.owner_company_id, self.company_a)
        self.assertEqual(grandchild.owner_company_id, self.company_a)

    def test_child_cannot_override_parent_owner(self):
        """A contact with a parent always takes the parent's owner company,
        no matter which owner is written on the contact itself."""
        child = self.env["res.partner"].create(
            {"name": "Owner Sync Child", "parent_id": self.parent_a.id}
        )
        child.write({"owner_company_id": self.company_b.id})
        self.assertEqual(child.owner_company_id, self.company_a)
        self.assertEqual(self.parent_a.owner_company_id, self.company_a)
        self.parent_a.write({"owner_company_id": False})
        child.write({"owner_company_id": self.company_b.id})
        self.assertFalse(child.owner_company_id)

    def test_batch_updates_preserve_each_parent_owner(self):
        """Writing an owner company on several children at once resolves
        each child against its own parent."""
        child_a = self.env["res.partner"].create(
            {"name": "Owner Sync Child A", "parent_id": self.parent_a.id}
        )
        child_b = self.env["res.partner"].create(
            {"name": "Owner Sync Child B", "parent_id": self.parent_b.id}
        )
        (child_a | child_b).write({"owner_company_id": False})
        self.assertEqual(child_a.owner_company_id, self.company_a)
        self.assertEqual(child_b.owner_company_id, self.company_b)

    def test_dropdown_follows_reparented_child(self):
        """Partial-name dropdown searches propose a reparented contact
        only under its new parent's company."""
        child = self.env["res.partner"].create(
            {
                "name": "Ownership Synchronization Contact",
                "parent_id": self.parent_a.id,
            }
        )
        child.write({"parent_id": self.parent_b.id})
        Partner = self.env["res.partner"].with_context(
            allowed_company_ids=(self.company_a | self.company_b).ids
        )
        company_a_results = Partner.with_company(self.company_a).name_search(
            "Ownership Synchronization"
        )
        company_b_results = Partner.with_company(self.company_b).name_search(
            "Ownership Synchronization"
        )
        company_a_ids = {result[0] for result in company_a_results}
        company_b_ids = {result[0] for result in company_b_results}
        self.assertNotIn(child.id, company_a_ids)
        self.assertIn(child.id, company_b_ids)

    def test_sync_from_grandchild_uses_top_level_owner(self):
        """Editing a grandchild repairs legacy ownership throughout its root's tree."""
        Partner = self.env["res.partner"]
        middle = Partner.create(
            {"name": "Owner Sync Middle", "parent_id": self.parent_a.id}
        )
        grandchild = Partner.create(
            {"name": "Owner Sync Grandchild", "parent_id": middle.id}
        )
        sibling = Partner.create(
            {"name": "Owner Sync Sibling", "parent_id": self.parent_a.id}
        )
        sibling.write({"active": False})
        legacy_contacts = middle | grandchild | sibling
        # Represent inconsistent ownership saved before synchronization existed.
        self.env.flush_all()
        self.env.cr.execute(
            "UPDATE res_partner SET owner_company_id = %s WHERE id IN %s",
            [self.company_b.id, tuple(legacy_contacts.ids)],
        )
        legacy_contacts.invalidate_recordset(["owner_company_id"])
        grandchild.write({"owner_company_id": False})
        for contact in self.parent_a | legacy_contacts:
            self.assertEqual(contact.owner_company_id, self.company_a)
        self.assertEqual(self.parent_b.owner_company_id, self.company_b)
