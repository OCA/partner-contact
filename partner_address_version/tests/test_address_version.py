# Copyright 2018 Akretion - Benoît Guillot
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import hashlib
from collections import OrderedDict
from contextlib import contextmanager

from mock import patch

from odoo.exceptions import UserError, ValidationError
from odoo.tests import SavepointCase

MOCK_PATH_RES_PARTNER = (
    "odoo.addons.partner_address_version" ".models.res_partner" ".ResPartner."
)


class TestAddressVersion(SavepointCase):
    @classmethod
    def _get_created_partners(cls):
        return (
            cls.env["res.partner"]
            .with_context(active_test=False)
            .search([("id", ">", cls.last_partner_id)], order="id desc")
        )

    @contextmanager
    def patch_fn(self, to_patch):
        """
        :param to_patch: dict of format function_name: return_value
        SavepointCase doesn't reset patched methods inbetween tests;
        we take care to clean them up
        """
        cleanup = []
        for path, return_value in to_patch.items():
            patcher = patch(MOCK_PATH_RES_PARTNER + path)
            mock_fn = patcher.start()
            mock_fn.return_value = return_value
            cleanup.append(patcher.stop)
        yield
        for stop_mock in cleanup:
            stop_mock()

    @classmethod
    def setUpClass(cls):
        super(TestAddressVersion, cls).setUpClass()
        cls.partner_vals = OrderedDict(
            [
                ("name", u"Name"),
                ("street", u"Street"),
                ("street2", u"Street2"),
                ("zip", u"Zip"),
                ("city", u"City"),
                ("country_id", cls.env.ref("base.fr")),
            ]
        )
        create_vals = cls.partner_vals.copy()
        create_vals["country_id"] = cls.env.ref("base.fr").id
        create_vals_2 = create_vals.copy()
        cls.partner = cls.env["res.partner"].create(create_vals)
        cls.partner_2 = cls.env["res.partner"].create(create_vals_2)
        cls.partner_vals.update({"parent_id": cls.partner.id})
        cls.last_partner_id = (
            cls.env["res.partner"]
            .with_context(active_test=False)
            .search([], order="id desc")[0]
            .id
            or 0
        )

    def test_hash(self):
        test_hash = hashlib.md5(str(self.partner_vals).encode("utf-8")).hexdigest()
        self.assertEqual(test_hash, self.partner._version_hash())

    def test_create_version_partner(self):
        new_partner = self.partner._version_create()
        self.assertEqual(new_partner.active, False)
        self.assertNotEqual(new_partner.id, self.partner.id)
        self.assertEqual(new_partner.parent_id.id, self.partner.id)

    def test_write_versioned_partner(self):
        new_partner = self.partner._version_create()
        with self.assertRaises(UserError):
            new_partner.street = "New street"

    def test_same_address_different_parent(self):
        new_partner = self.partner._version_create()
        new_partner_2 = self.partner_2._version_create()
        for field in self.partner._version_fields():
            if field == "parent_id":
                continue
            self.assertEqual(new_partner[field], new_partner_2[field])
        self.assertNotEqual(new_partner.id, new_partner_2.id)
        self.assertNotEqual(new_partner.version_hash, new_partner_2.version_hash)

    def test_version_exists(self):
        self.assertFalse(self.partner._version_exists())
        self.partner._version_create()
        self.assertTrue(self.partner._version_exists())

    def test_write_nonversioned_partner(self):
        """
        * Implement _version_need
        * Write on the partner
        -> We should get a new versioned partner
        """
        with self.patch_fn({"_version_need": True}):
            self.partner.street = "New Street"
        self.assertTrue(self._get_created_partners())

    def test_impacted_tables(self):
        """
        * Implement impacted_tables on res.users
        * Trigger partner versioning
        -> Check res.users are impacted
        """
        user = self.env.ref("base.user_demo")
        user.partner_id = self.partner
        with self.patch_fn(
            {
                "_version_need": True,
                "_version_impacted_tables": ["res_users"],
            }
        ):
            self.partner.street = "New Street"
        self.assertEqual(user.partner_id, self._get_created_partners())

    def test_impacted_tables_excluded_keys(self):
        """
        * Implement impacted_tables + excluded keys
        * Trigger partner versioning
        -> Check excluded keys are not affected
        """
        user = self.env.ref("base.user_demo")
        user.partner_id = self.partner
        with self.patch_fn(
            {
                "_version_need": True,
                "_version_impacted_tables": ["res_users"],
                "_version_exclude_keys": {"res_users": "partner_id"},
            }
        ):
            self.partner.street = "New Street"
        self.assertEqual(user.partner_id, self.partner)

    def test_impacted_columns(self):
        """
        * Implement impacted_columns
        * Trigger partner versioning
        -> Check res.users are impacted
        """
        user = self.env.ref("base.user_demo")
        user.partner_id = self.partner
        with self.patch_fn(
            {
                "_version_need": True,
                "_version_impacted_columns": [("res_users", "partner_id")],
            }
        ):
            self.partner.street = "New Street"
        self.assertEqual(user.partner_id, self._get_created_partners())

    def test_nonsense_implementation(self):
        """
        * Implement impacted_columns + Impacted_tables
        * Trigger partner versioning
        -> Error should occur
        """
        with self.patch_fn(
            {
                "_version_need": True,
                "_version_impacted_tables": ["res_users"],
                "_version_exclude_keys": {"res_users": "partner_id"},
                "_version_impacted_columns": [("res_users", "partner_id")],
            }
        ):
            with self.assertRaises(ValidationError):
                self.partner.street = "New Street"
