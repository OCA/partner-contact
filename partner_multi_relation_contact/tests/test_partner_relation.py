# Copyright 2026 Therp BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.exceptions import ValidationError

from .common import TestCommonCase


class TestPartnerRelation(TestCommonCase):
    def test_allow_contact(self):
        relation = self.company2person_relation
        relation_type = relation.type_id
        self.assertFalse(relation.allow_contact_partner)
        with self.assertRaises(ValidationError):
            self._action_contact_address(relation)
        # Now do allow email and phone, this should allow contact address.
        relation_type.write(
            {
                "allow_email": True,
                "allow_phone": True,
            }
        )
        self.assertTrue(relation_type.allow_contact_partner)
        self.assertTrue(relation.allow_contact_partner)
        # Should be possible to create contact address now.
        contact = self._action_contact_address(relation)
        self.assertEqual(contact.relation_id, relation)
        self.assertEqual(relation.contact_partner_id, contact)
