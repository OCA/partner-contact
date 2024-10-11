# Copyright 2015 ACSONE SA/NV (<https://acsone.eu>).
# Copyright 2016 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.base.tests.common import BaseCommon


class TestBasePartnerSequence(BaseCommon):
    def test_ref_sequence_on_partner(self):
        # Test sequence on creating partner and copying it
        self.assertTrue(self.partner.ref, "A partner has always a ref.")

        copy = self.partner.copy()
        self.assertTrue(
            copy.ref, "A partner with ref created by copy has a ref by default."
        )

    def test_ref_sequence_on_contact(self):
        # Test if sequence doesn't increase on creating a contact child
        contact = self.env["res.partner"].create(
            {
                "name": "contact1",
                "email": "contact@contact.com",
                "parent_id": self.partner.id,
            }
        )
        self.assertEqual(
            self.partner.ref, contact.ref, "All it's ok as sequence doesn't increase."
        )

    def test_unique_ref_on_write(self):
        """Assert that on create or on write, a different ref is assigned"""
        vals = [
            {"name": "test1", "email": "test@test.com"},
            {"name": "test2", "email": "test@test.com"},
        ]
        partners = self.env["res.partner"].create(vals)
        self.assertFalse(partners[0].ref == partners[1].ref)
        partners.write({"ref": False})
        self.assertFalse(partners[0].ref)
        partners.write({})
        self.assertFalse(partners[0].ref == partners[1].ref)

    def test_ref_change_convert_child_to_parent(self):
        """Test that a ref is assigned to a child contact when it is
        converted to a commercial partner."""
        # Remove the ref from the parent so child does not have one initially
        self.partner.write({"ref": False})
        contact = self.env["res.partner"].create(
            {
                "name": "contact1",
                "email": "contact@contact.com",
                "parent_id": self.partner.id,
            }
        )
        self.assertEqual(self.partner.ref, contact.ref)
        contact.write({"parent_id": False})
        self.assertTrue(contact.ref)
        self.assertFalse(contact.ref == self.partner.ref)
