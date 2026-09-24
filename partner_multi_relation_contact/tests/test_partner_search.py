# Copyright 2026 Therp BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.exceptions import ValidationError

from .common import TestCommonCase


class TestPartnerSearch(TestCommonCase):
    @classmethod
    def setUpClass(cls):
        """Main Set Up Class."""
        super().setUpClass()
        cls.type_company2person.write(
            {
                "allow_email": True,
                "allow_phone": True,
            }
        )

    def test_search_relation_phone(self):
        """Test searching for partners having a relation with a specific phone."""
        PHONE = "+31687654321"
        relation = self.company2person_relation
        self.assertTrue(relation.allow_contact_partner)
        contact = self._action_contact_address(relation)
        self.assertEqual(relation.contact_partner_id, contact)
        contact.write({"phone": PHONE})
        domain = [("search_relation_phone", "=", PHONE), ("type", "=", "contact")]
        partners = self.Partner.search(domain)
        self.assertEqual(len(partners), 2)
        self.assertTrue(self.partner_02_company in partners)
        self.assertTrue(self.partner_01_person in partners)
        # Try search with invalid operator
        domain = [("search_relation_phone", "child_of", PHONE)]
        with self.assertRaises(ValidationError):
            self.Partner.search(domain)
        # Search for non existing phone.
        domain = [("search_relation_phone", "=", "not an existing phonenumber")]
        partners = self.Partner.search(domain)
        self.assertEqual(len(partners), 0)

    def test_search_relation_email(self):
        """Test searching for partners having a relation with a specific email."""
        EMAIL = "head_of_legal@bigcompany.example.com"
        relation = self.company2person_relation
        self.assertTrue(relation.allow_contact_partner)
        contact = self._action_contact_address(relation)
        self.assertEqual(relation.contact_partner_id, contact)
        contact.write({"email": EMAIL})
        domain = [("search_relation_email", "=", EMAIL), ("type", "=", "contact")]
        partners = self.Partner.search(domain)
        self.assertEqual(len(partners), 2)
        self.assertTrue(self.partner_02_company in partners)
        self.assertTrue(self.partner_01_person in partners)
        # Try search with invalid operator
        domain = [("search_relation_email", "child_of", EMAIL)]
        with self.assertRaises(ValidationError):
            self.Partner.search(domain)
        # Search for non existing email.
        domain = [("search_relation_email", "=", "notexisting@bigcompany.example.com")]
        partners = self.Partner.search(domain)
        self.assertEqual(len(partners), 0)
