# Copyright 2015 Camptocamp SA
# Copyright 2016-2020 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Test methods added to res.partner model."""
from odoo import fields
from odoo.exceptions import ValidationError

from .common import PartnerRelationCase


class TestPartnerSearch(PartnerRelationCase):
    """Test methods added to res.partner model."""

    def test_search_relation_type(self):
        """Test searching on relation type."""
        partners = self.partner_model.search(
            [("search_relation_type_id", "=", self.selection_company_has_employee.id)]
        )
        self.assertTrue(self.partner_company_test in partners)
        partners = self.partner_model.search(
            [("search_relation_type_id", "!=", self.selection_company_has_employee.id)]
        )
        self.assertTrue(self.partner_person_test in partners)
        partners = self.partner_model.search(
            [
                (
                    "search_relation_type_id",
                    "=",
                    self.relation_type_company_has_employee.name,
                )
            ]
        )
        self.assertTrue(self.partner_company_test in partners)
        self.assertTrue(self.partner_person_test in partners)
        partners = self.partner_model.search(
            [("search_relation_type_id", "=", "unknown relation")]
        )
        self.assertFalse(partners)
        # Check error with invalid search operator:
        with self.assertRaises(ValidationError):
            partners = self.partner_model.search(
                [("search_relation_type_id", "child_of", "some parent")]
            )

    def test_search_relation_partner(self):
        """Test searching on related partner."""
        partners = self.partner_model.search(
            [("search_relation_partner_id", "=", self.partner_company_test.id)]
        )
        self.assertTrue(self.partner_person_test in partners)

    def test_search_relation_date(self):
        """Test searching on relations valid on a certain date."""
        partners = self.partner_model.search(
            [("search_relation_date", "=", fields.Date.today())]
        )
        self.assertTrue(self.partner_company_test in partners)
        self.assertTrue(self.partner_person_test in partners)

    def test_search_any_partner(self):
        """Test searching for partner left or right."""
        both_relations = self.relation_all_model.search(
            [("any_partner_id", "=", self.partner_company_test.id)]
        )
        self.assertEqual(len(both_relations), 2)

    def test_search_partner_category(self):
        """Test searching for partners related to partners having category."""
        partners = self.partner_model.search(
            [("search_relation_partner_category_id", "=", self.category_volunteer.id)]
        )
        self.assertTrue(self.partner_ngo_test in partners)
