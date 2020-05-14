# Copyright 2015 Camptocamp SA
# Copyright 2016 Therp BV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields
from odoo.exceptions import ValidationError

from .test_partner_relation_common import TestPartnerRelationCommon


class TestPartnerSearch(TestPartnerRelationCommon):
    def test_search_relation_type(self):
        """Test searching on relation type."""
        relation = self._create_company2person_relation()
        partners = self.partner_model.search(
            [("search_relation_type_id", "=", relation.type_selection_id.id)]
        )
        self.assertTrue(self.partner_02_company in partners)
        partners = self.partner_model.search(
            [("search_relation_type_id", "!=", relation.type_selection_id.id)]
        )
        self.assertTrue(self.partner_01_person in partners)
        partners = self.partner_model.search(
            [("search_relation_type_id", "=", self.type_company2person.name)]
        )
        self.assertTrue(self.partner_01_person in partners)
        self.assertTrue(self.partner_02_company in partners)
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
        self._create_company2person_relation()
        partners = self.partner_model.search(
            [("search_relation_partner_id", "=", self.partner_02_company.id)]
        )
        self.assertTrue(self.partner_01_person in partners)

    def test_search_relation_date(self):
        """Test searching on relations valid on a certain date."""
        self._create_company2person_relation()
        partners = self.partner_model.search(
            [("search_relation_date", "=", fields.Date.today())]
        )
        self.assertTrue(self.partner_01_person in partners)
        self.assertTrue(self.partner_02_company in partners)

    def test_search_any_partner(self):
        """Test searching for partner left or right."""
        self._create_company2person_relation()
        both_relations = self.relation_all_model.search(
            [("any_partner_id", "=", self.partner_02_company.id)]
        )
        self.assertEqual(len(both_relations), 2)

    def test_search_partner_category(self):
        """Test searching for partners related to partners having category."""
        relation_ngo_volunteer = self.relation_all_model.create(
            {
                "this_partner_id": self.partner_03_ngo.id,
                "type_selection_id": self.selection_ngo2volunteer.id,
                "other_partner_id": self.partner_04_volunteer.id,
            }
        )
        self.assertTrue(relation_ngo_volunteer)
        partners = self.partner_model.search(
            [
                (
                    "search_relation_partner_category_id",
                    "=",
                    self.category_02_volunteer.id,
                )
            ]
        )
        self.assertTrue(self.partner_03_ngo in partners)
