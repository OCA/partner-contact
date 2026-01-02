# Copyright 2026 Therp BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.exceptions import ValidationError
from odoo.tests import common


class TestPartnerSearch(common.TransactionCase):
    def test_search_relation_function(self):
        """Test searching for partners having a relation with a specific function."""
        Partner = self.env["res.partner"]
        RelationType = self.env["res.partner.relation.type"]
        Relation = self.env["res.partner.relation"]
        partner_person = Partner.create(
            {"name": "Test Participant", "is_company": False, "ref": "PR01"}
        )
        partner_project = Partner.create(
            {"name": "Test Project", "is_company": True, "ref": "PR02"}
        )
        type_with_function = RelationType.create(
            {
                "name": "project has participant",
                "name_inverse": "participates in project",
                "contact_type_left": "c",
                "contact_type_right": "p",
                "allow_function": True,
            }
        )
        relation_with_function = Relation.create(
            {
                "left_partner_id": partner_project.id,
                "type_id": type_with_function.id,
                "function": "coordinator",
                "right_partner_id": partner_person.id,
            }
        )
        self.assertTrue(relation_with_function)
        domain = [("search_relation_function", "=", "coordinator")]
        partners = Partner.search(domain)
        self.assertEqual(len(partners), 2)
        self.assertTrue(partner_project in partners)
        self.assertTrue(partner_person in partners)
        # Try search with invalid operator
        domain = [("search_relation_function", "child_of", "coordinator")]
        with self.assertRaises(ValidationError):
            Partner.search(domain)
        # Search for non existing function.
        domain = [("search_relation_function", "=", "not an existing function")]
        partners = Partner.search(domain)
        self.assertEqual(len(partners), 0)
