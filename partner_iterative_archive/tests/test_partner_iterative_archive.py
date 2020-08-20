# Copyright 2019-2020 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestBase(TransactionCase):
    def setUp(self):
        super().setUp()
        Partner = self.env["res.partner"]
        self.p1 = Partner.browse(Partner.name_create("Parent")[0])
        self.c1 = Partner.create({"name": "Child 1", "parent_id": self.p1.id})
        self.c11 = Partner.create({"name": "Grand-Child 1.1", "parent_id": self.c1.id})
        self.c2 = Partner.create({"name": "Child 2", "parent_id": self.p1.id})

    def test_01_archive_partners(self):
        self.assertTrue(self.p1.active)
        self.assertTrue(self.c1.active)
        self.assertTrue(self.c11.active)
        self.assertTrue(self.c2.active)

        # archive the parent partner, skip the archive of contacts
        self.p1.with_context(skip_child_toggle_active=True).toggle_active()
        self.assertFalse(self.p1.active)
        self.assertTrue(self.c1.active)
        self.assertTrue(self.c11.active)
        self.assertTrue(self.c2.active)

        # unarchive the parent partner
        self.p1.toggle_active()
        self.assertTrue(self.c1.active)
        self.assertTrue(self.c11.active)
        self.assertTrue(self.c2.active)

        # archive the parent partner, automatically archive contacts
        self.p1.toggle_active()
        self.assertFalse(self.p1.active)
        self.assertFalse(self.c1.active)
        self.assertFalse(self.c11.active)
        self.assertFalse(self.c2.active)

        # unarchive the parent partner
        self.p1.toggle_active()
        self.assertTrue(self.p1.active)
        self.assertFalse(self.c1.active)
        self.assertFalse(self.c11.active)
        self.assertFalse(self.c2.active)
