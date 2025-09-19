# Copyright 2015 Camptocamp SA.
# Copyright 2016-2025 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import timedelta

from odoo import fields
from odoo.exceptions import ValidationError

from .test_partner_relation_common import TestPartnerRelationCommon


class TestPartnerSearch(TestPartnerRelationCommon):
    def test_search_type(self):
        """Test searching on relation type."""
        relation = self.company2person_relation
        partners = self.Partner.search(
            [("search_relation_type_id", "=", relation.type_id.id)]
        )
        self.assertTrue(self.partner_02_company in partners)
        self.assertTrue(self.partner_01_person in partners)
        partners = self.Partner.search(
            [("search_relation_type_id", "=", self.type_company2person.name)]
        )
        self.assertTrue(self.partner_01_person in partners)
        self.assertTrue(self.partner_02_company in partners)
        partners = self.Partner.search(
            [("search_relation_type_id", "=", "unknown relation")]
        )
        self.assertFalse(partners)
        # Check error with invalid search operator:
        with self.assertRaises(ValidationError):
            partners = self.Partner.search(
                [("search_relation_type_id", "child_of", "some parent")]
            )

    def test_get_domain_relation_search(self):
        """Test searching on related partner."""
        domain = [
            ("search_relation_partner_id", "=", self.partner_02_company.id),
            ("search_relation_date", "=", fields.Date.today()),
            ("name", "ilike", "user"),
        ]
        relation_search = self.Partner._get_domain_relation_search(domain)
        self.assertIn("search_relation_partner_id", relation_search)
        self.assertIn("search_relation_date", relation_search)
        self.assertNotIn("name", relation_search)

    def test_update_domain_relation_search(self):
        """Check injection of date and active, when updating domain."""
        domain = [("search_relation_partner_id", "=", self.partner_02_company.id)]
        relation_search = self.Partner._get_domain_relation_search(domain)
        self.assertEqual(relation_search, ["search_relation_partner_id"])
        domain = self.Partner._update_domain_relation_search(domain, relation_search)
        self.assertIn(("relation_right_ids.active", "=", True), domain)
        relation_search = self.Partner._get_domain_relation_search(domain)
        self.assertIn("search_relation_date", relation_search)

    def test_search_relation_partner(self):
        """Test searching on related partner."""
        partners = self.Partner.search(
            [("search_relation_partner_id", "=", self.partner_02_company.id)]
        )
        self.assertTrue(self.partner_01_person in partners)

    def test_search_relation_date_today(self):
        """Test searching on relations valid on a certain date."""
        partners = self.Partner.search(
            [("search_relation_date", "=", fields.Date.today())]
        )
        self.assertTrue(self.partner_01_person in partners)
        self.assertTrue(self.partner_02_company in partners)

    def test_search_relation_date_future(self):
        """Test searching on relations valid on a certain date."""
        today = fields.Date.today()
        one_day = timedelta(days=1)
        tomorrow = today + one_day
        day_after_tomorrow = tomorrow + one_day
        great_company = self.Partner.create(
            {"name": "Great Company", "is_company": True, "ref": "GRTCOM"}
        )
        hard_working_person = self.Partner.create(
            {"name": "Hard Working Person", "is_company": False, "ref": "HRDWRK"}
        )
        self.Relation.create(
            {
                "left_partner_id": great_company.id,
                "type_id": self.type_company2person.id,
                "right_partner_id": hard_working_person.id,
                "date_start": tomorrow,
                "date_end": False,
            }
        )
        partners = self.Partner.search([("search_relation_date", "=", today)])
        self.assertTrue(self.partner_01_person in partners)
        self.assertTrue(self.partner_02_company in partners)
        self.assertFalse(great_company in partners)
        self.assertFalse(hard_working_person in partners)
        self.company2person_relation.write({"date_end": today})
        partners = self.Partner.search(
            [("search_relation_date", "=", day_after_tomorrow)]
        )
        self.assertFalse(self.partner_01_person in partners)
        self.assertFalse(self.partner_02_company in partners)
        self.assertTrue(great_company in partners)
        self.assertTrue(hard_working_person in partners)

    def test_search_active_inactive(self):
        """Test searching on partners with active and inactive relations."""
        domain = [("search_relation_type_id", "=", self.type_company2person.name)]
        partners = self.Partner.search(domain)
        self.assertTrue(self.partner_01_person in partners)
        self.assertTrue(self.partner_02_company in partners)
        relation = self.company2person_relation
        relation.write({"active": False})
        partners = self.Partner.search(domain)
        self.assertFalse(self.partner_01_person in partners)
        self.assertFalse(self.partner_02_company in partners)
        # Same if we explicitly pass active_test=True.
        partners = self.Partner.with_context(active_test=True).search(domain)
        self.assertFalse(self.partner_01_person in partners)
        self.assertFalse(self.partner_02_company in partners)
        partners = self.Partner.with_context(active_test=False).search(domain)
        self.assertTrue(self.partner_01_person in partners)
        self.assertTrue(self.partner_02_company in partners)

    def test_search_any_partner(self):
        """Test searching for partner that has a relation with searched partner."""
        partners = self.Partner.search(
            [("search_relation_partner_id", "ilike", "user")]
        )
        self.assertIn(self.partner_02_company, partners)

    def test_search_partner_category(self):
        """Test searching for partners related to partners having category."""
        relation_ngo_volunteer = self.Relation.create(
            {
                "left_partner_id": self.partner_03_ngo.id,
                "type_id": self.type_ngo2volunteer.id,
                "right_partner_id": self.partner_04_volunteer.id,
            }
        )
        self.assertTrue(relation_ngo_volunteer)
        partners = self.Partner.search(
            [
                (
                    "search_relation_partner_category_id",
                    "=",
                    self.category_02_volunteer.id,
                )
            ]
        )
        self.assertTrue(self.partner_03_ngo in partners)
