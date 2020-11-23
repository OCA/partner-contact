# Copyright 2018 Akretion - Benoît Guillot
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import hashlib
from collections import OrderedDict

from odoo.exceptions import UserError
from odoo.tests import SavepointCase


class TestAddressVersion(SavepointCase):
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
