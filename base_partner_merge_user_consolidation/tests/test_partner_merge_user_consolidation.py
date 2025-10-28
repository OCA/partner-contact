# Copyright 2025 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import timedelta

from odoo import Command, fields
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestMergePartnerUsers(TransactionCase):
    @classmethod
    def setUpClass(cls):
        # sudo the multiverse here, just in case
        super().setUpClass()
        cls.Partner = cls.env["res.partner"].sudo()
        cls.User = cls.env["res.users"].sudo()
        cls.Groups = cls.env["res.groups"].sudo()
        cls.Log = cls.env["res.users.log"].sudo()
        cls.Wizard = cls.env["base.partner.merge.automatic.wizard"].sudo()
        cls.grp_partner_manager = cls.env.ref("base.group_partner_manager")
        cls.grp_no_one = cls.env.ref("base.group_no_one")
        # create users with different groups, for merging
        cls.p1 = cls.Partner.create(
            {"name": "Data", "is_company": False, "email": "data@deepspace.nine"}
        )
        cls.p2 = cls.Partner.create(
            {"name": "Lore.", "is_company": False, "email": "lore@deepspace.nine"}
        )
        cls.u1 = cls.User.create(
            {
                "name": "User Data",
                "login": "data@deepspace.nine",
                "partner_id": cls.p1.id,
                "groups_id": [(4, cls.grp_partner_manager.id)],
            }
        )
        cls.u2 = cls.User.create(
            {
                "name": "User Lore",
                "login": "lore@deepspace.nine",
                "partner_id": cls.p2.id,
                "groups_id": [(4, cls.grp_no_one.id)],
            }
        )

        # Mimic login
        older_log = cls.Log.with_user(cls.u1).create({})
        older = fields.Datetime.now() - timedelta(days=10)
        # needed to actually invoke raw sql for this
        cls.env.cr.execute(
            "UPDATE res_users_log SET create_date = %s WHERE id = %s",
            (fields.Datetime.to_string(older), older_log.id),
        )
        # Data will be merged into Lore
        cls.Log.with_user(cls.u2).create({})

    def _fresh(self):
        self.env.invalidate_all()
        return (
            self.Partner.browse(self.p1.id),
            self.Partner.browse(self.p2.id),
            self.User.browse(self.u1.id),
            self.User.browse(self.u2.id),
        )

    def test_merge_user(self):
        """Merge partner AND user, unlink partner, archive user"""
        wiz = self.Wizard.create({})
        wiz._merge([self.p1.id, self.p2.id], dst_partner=self.p1)
        # source partner removed
        self.assertFalse(self.p2.exists())
        # fresh read
        self.env.invalidate_all()
        self.assertEqual(self.u2.partner_id.id, self.p1.id)
        self.assertTrue(self.u2.active)
        self.assertFalse(self.u1.active)
        # defuse everything for obsolete user
        self.assertTrue(self.u1.login.startswith("__merged_user_"))
        kept_groups = set(self.u2.groups_id.ids)
        self.assertIn(self.grp_partner_manager.id, kept_groups)
        self.assertIn(self.grp_no_one.id, kept_groups)

    def test_noop_single_user(self):
        """If only one user across both partners, no consolidation."""
        # Fresh partners, only one user attached overall
        p3 = self.Partner.create({"name": "Duncan", "email": "Duncan@Duncan.com"})
        p4 = self.Partner.create({"name": "Connor", "email": "Connor@Connor.com"})
        u = self.User.create(
            {
                "name": "there can be only one",
                "login": "theone@theone.com",
                "partner_id": p3.id,
            }
        )
        wiz = self.Wizard.create({})
        wiz._merge([p3.id, p4.id], dst_partner=p3)
        self.env.invalidate_all()
        self.assertFalse(p4.exists())
        self.assertTrue(u.exists())
        self.assertTrue(u.active)
        self.assertEqual(u.partner_id.id, p3.id)

    def test_pick_latest_login_kept(self):
        """User with newest login_date is kept"""
        p1, p2, u1, u2 = self._fresh()
        wiz = self.Wizard.create({})
        wiz._merge([p1.id, p2.id], dst_partner=p1)
        p1, p2, u1, u2 = self._fresh()
        self.assertTrue(u2.active)
        self.assertFalse(u1.active)
        self.assertEqual(u2.partner_id.id, p1.id)

    def test_create_date_when_no_logs(self):
        """If neither user has login logs, fall back to create_date ordering."""
        pa = self.Partner.create({"name": "A", "email": "a@a.a"})
        pb = self.Partner.create({"name": "B", "email": "b@b.b"})
        ua = self.User.create({"name": "A", "login": "a@a.a", "partner_id": pa.id})
        ub = self.User.create({"name": "B", "login": "b@b.b", "partner_id": pb.id})
        # No logs
        self.env.cr.execute(
            "DELETE FROM res_users_log WHERE create_uid IN %s", ((ua.id, ub.id),)
        )
        wiz = self.Wizard.create({})
        wiz._merge([pa.id, pb.id], dst_partner=pa)
        self.env.invalidate_all()
        ua, ub = self.User.browse(ua.id), self.User.browse(ub.id)
        # last person survives
        self.assertTrue(ub.active)
        self.assertFalse(ua.active)
        self.assertEqual(ub.partner_id.id, pa.id)

    def test_dst_partner_autoselection_when_not_provided(self):
        """When dst_partner isn't provided, wizard picks ordered[-1
        ] and still consolidates users."""
        pa = self.Partner.create({"name": "A", "email": "a@a.a"})
        pb = self.Partner.create({"name": "B", "email": "b@b.b"})
        ua = self.User.create({"name": "A", "login": "a@a.a", "partner_id": pa.id})
        ub = self.User.create({"name": "B", "login": "b@b.b", "partner_id": pb.id})
        # Make ub newest by login
        self.Log.with_user(ub).create({})
        wiz = self.Wizard.create({})
        wiz._merge([pa.id, pb.id])  # no dst_partner
        self.env.invalidate_all()
        pa, pb, ua, ub = (
            self.Partner.browse(pa.id),
            self.Partner.browse(pb.id),
            self.User.browse(ua.id),
            self.User.browse(ub.id),
        )
        survivor = pa if pa.exists() else pb
        self.assertEqual(ub.partner_id.id, survivor.id)
        self.assertTrue(ub.active)
        self.assertFalse(ua.active)

    def test_group_union_and(self):
        """Union groups from losing"""
        cat = self.env["ir.module.category"].sudo().create({"name": "Test Implied"})
        g2 = self.Groups.create({"name": "implied", "category_id": cat.id})
        g1 = self.Groups.create({"name": "parent", "category_id": cat.id})
        g1.write({"implied_ids": [Command.link(g2.id)]})
        pa = self.Partner.create({"name": "A", "email": "a@a.a"})
        pb = self.Partner.create({"name": "B", "email": "b@b.b"})
        self.User.create(
            {
                "name": "A",
                "login": "a@a.a",
                "partner_id": pa.id,
                "groups_id": [Command.link(g2.id)],
            }
        )
        ub = self.User.create(
            {
                "name": "B",
                "login": "b@b.b",
                "partner_id": pb.id,
                "groups_id": [Command.link(g1.id)],
            }
        )
        # user B is kept
        self.Log.with_user(ub).create({})
        wiz = self.Wizard.create({})
        wiz._merge([pa.id, pb.id], dst_partner=pa)
        self.env.invalidate_all()
        ub = self.User.browse(ub.id)
        gids = set(ub.groups_id.ids)
        self.assertIn(g1.id, gids)
        self.assertIn(g2.id, gids)

    def test_archive_user_login(self):
        """Obsolete users get inactive and their login is scrambled"""
        p1, p2, u1, u2 = self._fresh()
        wiz = self.Wizard.create({})
        wiz._merge([p1.id, p2.id], dst_partner=p1)
        self.env.invalidate_all()
        u1 = self.User.browse(u1.id)
        self.assertFalse(u1.active)
        self.assertTrue(u1.login.startswith(f"__merged_user_{u1.id}_"))
        self.assertNotEqual(u1.login, "data@deepspace.nine")

    def test_extra_checks_different_emails_raise_for_non_admin(self):
        """Raise when there is a difference in emails and user is not admin"""
        # Create a normal internal user
        mgr_partner = self.Partner.create({"name": "Buzz Lightyear"})
        mgr = (
            self.env["res.users"]
            .with_context(no_reset_password=True)
            .create(
                {
                    "name": "Buzz Lightyear",
                    "login": "mgr@example.com",
                    "partner_id": mgr_partner.id,
                    # enable wizard
                    "groups_id": [
                        Command.link(self.env.ref("base.group_user").id),
                        Command.link(self.grp_partner_manager.id),
                    ],
                }
            )
        )

        a = self.Partner.create({"name": "A", "email": "a@a.a"})
        b = self.Partner.create({"name": "B", "email": "b@b.b"})
        wiz = self.env["base.partner.merge.automatic.wizard"].with_user(mgr).create({})
        with self.assertRaises(UserError):
            wiz._merge([a.id, b.id])
