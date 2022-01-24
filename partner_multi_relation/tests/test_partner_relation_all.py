# Copyright 2016-2021 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
"""Test res.partner.relation.all, the main model to interface with relations."""
import datetime
import json

from odoo.exceptions import ValidationError

from .common import PartnerRelationCase


class TestPartnerRelation(PartnerRelationCase):
    """Test res.partner.relation.all, the main model to interface with relations."""

    def setUp(self):
        super().setUp()

        # Another partner.
        self.partner_bart = self.partner_model.create(
            {"name": "Bart Simpson", "is_company": False, "ref": "BS"}
        )
        # Create a new relation type, to prevent overlap with demo data.
        self.relation_type_company_has_ceo = self.type_model.create(
            {
                "name": "has ceo",
                "name_inverse": "is ceo of",
                "contact_type_left": "c",
                "contact_type_right": "p",
            }
        )
        self.selection_company_has_ceo = self._get_selection_type(
            self.relation_type_company_has_ceo, is_inverse=False
        )
        self.selection_person_is_ceo = self._get_selection_type(
            self.relation_type_company_has_ceo, is_inverse=True
        )
        # Create a new relation type which will not have valid relations.
        category_nobody = self.category_model.create({"name": "Nobody"})
        self.relation_type_nobody = self.type_model.create(
            {
                "name": "has relation with nobody",
                "name_inverse": "nobody has relation with",
                "contact_type_left": "c",
                "contact_type_right": "p",
                "partner_category_left": category_nobody.id,
                "partner_category_right": category_nobody.id,
            }
        )
        self.selection_nobody = self._get_selection_type(
            self.relation_type_nobody, is_inverse=False
        )
        # Create a ceo relation
        self.relation_ceo = self.relation_all_model.create(
            {
                "this_partner_id": self.partner_company_test.id,
                "type_selection_id": self.selection_company_has_ceo.id,
                "other_partner_id": self.partner_person_test.id,
            }
        )

    def _get_empty_relation(self):
        """Get empty relation record for onchange tests."""
        # Need English, because we will compare text
        return self.relation_all_model.with_context(lang="en_US").new({})

    def test_get_partner_types(self):
        """Partner types should contain at least 'c' and 'p'."""
        partner_types = self.selection_model.get_partner_types()
        type_codes = [ptype[0] for ptype in partner_types]
        self.assertTrue("c" in type_codes)
        self.assertTrue("p" in type_codes)

    def test_create_with_active_id(self):
        """Test creation with this_partner_id from active_id."""
        # Check wether we can create connection from company to person,
        # taking the particular company from the active records:
        relation = self.relation_all_model.with_context(
            active_id=self.partner_company_test.id,
            active_ids=self.partner_company_test.ids,
        ).create(
            {
                "other_partner_id": self.partner_bart.id,
                "type_selection_id": self.selection_company_has_employee.id,
            }
        )
        self.assertTrue(relation)
        self.assertEqual(relation.this_partner_id, self.partner_company_test)
        # Partner should have one relation now:
        self.assertEqual(self.partner_bart.relation_count, 1)
        # Test create without type_selection_id:
        with self.assertRaises(ValidationError):
            self.relation_all_model.create(
                {
                    "this_partner_id": self.partner_company_test.id,
                    "other_partner_id": self.partner_bart.id,
                }
            )

    def test_display_name(self):
        """Test display name"""
        relation = self.relation_ceo
        self.assertEqual(
            relation.display_name,
            "%s %s %s"
            % (
                relation.this_partner_id.name,
                relation.type_selection_id.name,
                relation.other_partner_id.name,
            ),
        )

    def test_active_field(self):
        """Test compute and search of active field."""
        underlying_relation = self.relation_company2employee
        relation = underlying_relation.get_derived_relation()
        # We have to find the right relation.all record for the relation record.
        self.assertTrue(relation.active)
        # If we search on active records for this partner, we should find record.
        domain = [
            ("this_partner_id", "=", relation.this_partner_id.id),
            ("active", "=", True),
        ]
        relations_found = self.relation_all_model.search(domain)
        self.assertIn(relation, relations_found)
        # If we set the enddate to a date in the past, active should become False.
        relation.date_end = "1999-12-31"
        self.assertFalse(relation.active)
        relations_found = self.relation_all_model.search(domain)
        self.assertNotIn(relation, relations_found)
        # Inactive should be found with inactive records.
        domain = [
            ("this_partner_id", "=", relation.this_partner_id.id),
            ("active", "!=", True),
        ]
        relations_found = self.relation_all_model.search(domain)
        self.assertIn(relation, relations_found)
        # Clear enddate. Relation should become active again.
        relation.date_end = False
        self.assertTrue(relation.active)
        relations_found = self.relation_all_model.search(domain)
        self.assertNotIn(relation, relations_found)

    def test__regular_write(self):
        """Test write with valid data."""
        compare_date = datetime.date(2014, 9, 1)
        self.relation_ceo.write({"date_start": "2014-09-01"})
        self.assertEqual(self.relation_ceo.date_start, compare_date)

    def test_write_incompatible_dates(self):
        """Test write with date_end before date_start."""
        relation = self.relation_ceo
        with self.assertRaises(ValidationError):
            relation.write({"date_start": "2016-09-01", "date_end": "2016-08-01"})

    def test_validate_overlapping_01(self):
        """Test create overlapping with no start / end dates."""
        relation = self.relation_ceo
        with self.assertRaises(ValidationError):
            # New relation with no start / end should give error
            self.relation_all_model.create(
                {
                    "this_partner_id": relation.this_partner_id.id,
                    "type_selection_id": relation.type_selection_id.id,
                    "other_partner_id": relation.other_partner_id.id,
                }
            )

    def test_validate_overlapping_02(self):
        """Test create overlapping with start / end dates."""
        relation = self.relation_all_model.create(
            {
                "this_partner_id": self.partner_company_test.id,
                "type_selection_id": self.selection_company_has_employee.id,
                "other_partner_id": self.partner_bart.id,
                "date_start": "2015-09-01",
                "date_end": "2016-08-31",
            }
        )
        # New relation with overlapping start / end should give error
        with self.assertRaises(ValidationError):
            self.relation_all_model.create(
                {
                    "this_partner_id": relation.this_partner_id.id,
                    "type_selection_id": relation.type_selection_id.id,
                    "other_partner_id": relation.other_partner_id.id,
                    "date_start": "2016-08-01",
                    "date_end": "2017-07-30",
                }
            )

    def test_validate_overlapping_03(self):
        """Test create not overlapping."""
        relation = self.relation_all_model.create(
            {
                "this_partner_id": self.partner_company_test.id,
                "type_selection_id": self.selection_company_has_employee.id,
                "other_partner_id": self.partner_bart.id,
                "date_start": "2015-09-01",
                "date_end": "2016-08-31",
            }
        )
        relation_another_record = self.relation_all_model.create(
            {
                "this_partner_id": relation.this_partner_id.id,
                "type_selection_id": relation.type_selection_id.id,
                "other_partner_id": relation.other_partner_id.id,
                "date_start": "2016-09-01",
                "date_end": "2017-08-31",
            }
        )
        self.assertTrue(relation_another_record)

    def test_inverse_record(self):
        """Test creation of inverse record."""
        # relation_ceo is from company to ceo.
        relation = self.relation_ceo
        self.assertEqual(relation.type_selection_id.name, "has ceo")
        inverse_relation = self.relation_all_model.search(
            [
                ("this_partner_id", "=", relation.other_partner_id.id),
                ("type_id", "=", self.relation_type_company_has_ceo.id),
                ("other_partner_id", "=", relation.this_partner_id.id),
            ],
            limit=1,
        )
        self.assertTrue(bool(inverse_relation))
        self.assertEqual(inverse_relation.type_selection_id.name, "is ceo of")

    def test_inverse_creation(self):
        """Test creation of record through inverse selection."""
        relation = self.relation_all_model.create(
            {
                "this_partner_id": self.partner_bart.id,
                "type_selection_id": self.selection_person_is_ceo.id,
                "other_partner_id": self.partner_company_test.id,
            }
        )
        # Check wether display name is what we should expect:
        self.assertEqual(
            relation.display_name,
            "%s %s %s"
            % (
                self.partner_bart.name,
                self.selection_person_is_ceo.name,
                self.partner_company_test.name,
            ),
        )

    def test_inverse_creation_type_id(self):
        """Test creation of record through inverse selection with type_id."""
        relation = self.relation_all_model.create(
            {
                "this_partner_id": self.partner_bart.id,
                "type_id": self.selection_person_is_ceo.type_id.id,
                "is_inverse": True,
                "other_partner_id": self.partner_company_test.id,
            }
        )
        # Check wether display name is what we should expect:
        self.assertEqual(
            relation.display_name,
            "%s %s %s"
            % (
                self.partner_bart.name,
                self.selection_person_is_ceo.name,
                self.partner_company_test.name,
            ),
        )

    def test_unlink(self):
        """Unlinking derived relation should unlink base relation."""
        # Check wether underlying record is removed when record is removed:
        relation = self.relation_ceo
        base_model = self.env[relation.res_model]
        base_relation = base_model.browse([relation.res_id])
        relation.unlink()
        self.assertFalse(base_relation.exists())
        # Check unlinking record sets with both derived relation records
        self.assertTrue(self.relation_all_model.search([]).unlink())

    def test_on_change_type_selection(self):
        """Test on_change_type_selection."""
        # 1. Test call with empty relation
        relation_empty = self._get_empty_relation()
        result = relation_empty.onchange_type_selection_id()
        self.assertTrue("domain" in result)
        self.assertFalse("warning" in result)
        # TODO: We should be able to predict the exact domains for partners.
        self.assertTrue("this_partner_id" in result["domain"])
        self.assertTrue(result["domain"]["this_partner_id"])
        self.assertTrue("other_partner_id" in result["domain"])
        self.assertTrue(result["domain"]["other_partner_id"])
        # 2. Test call with company 2 person relation
        relation = self.relation_ceo
        domain = relation.onchange_type_selection_id()["domain"]
        self.assertTrue(("is_company", "=", False) in domain["other_partner_id"])
        # 3. Test with relation needing categories,
        #    take active partner from active_id:
        relation_ngo_volunteer = self.relation_all_model.search(
            [("type_selection_id", "=", self.selection_ngo_has_volunteer.id)], limit=1
        )
        domain = relation_ngo_volunteer.onchange_type_selection_id()["domain"]
        self.assertTrue(
            ("category_id", "in", [self.category_ngo.id]) in domain["this_partner_id"]
        )
        self.assertTrue(
            ("category_id", "in", [self.category_volunteer.id])
            in domain["other_partner_id"]
        )
        # 4. Test with invalid or impossible combinations
        relation_nobody = self._get_empty_relation()
        with self.env.do_in_draft():
            relation_nobody.type_selection_id = self.selection_nobody
        warning = relation_nobody.onchange_type_selection_id()["warning"]
        self.assertTrue("message" in warning)
        self.assertTrue("No this partner available" in warning["message"])
        with self.env.do_in_draft():
            relation_nobody.this_partner_id = self.partner_company_test
        warning = relation_nobody.onchange_type_selection_id()["warning"]
        self.assertTrue("message" in warning)
        self.assertTrue("incompatible" in warning["message"])
        # Allow left partner and check message for other partner:
        self.relation_type_nobody.write({"partner_category_left": False})
        self.selection_nobody.invalidate_cache(ids=self.selection_nobody.ids)
        warning = relation_nobody.onchange_type_selection_id()["warning"]
        self.assertTrue("message" in warning)
        self.assertTrue("No other partner available" in warning["message"])

    def test_on_change_partner_id(self):
        """Test on_change_partner_id."""
        # 1. Test call with empty relation
        relation_empty = self._get_empty_relation()
        result = relation_empty.onchange_partner_id()
        self.assertTrue("domain" in result)
        self.assertFalse("warning" in result)
        self.assertTrue("type_selection_id" in result["domain"])
        self.assertFalse(result["domain"]["type_selection_id"])
        # 2. Test call with company 2 person relation
        relation = self.relation_ceo
        domain = relation.onchange_partner_id()["domain"]
        self.assertTrue(("contact_type_this", "=", "c") in domain["type_selection_id"])
        # 3. Test with invalid or impossible combinations
        relation_nobody = self._get_empty_relation()
        with self.env.do_in_draft():
            relation_nobody.this_partner_id = self.partner_company_test
            relation_nobody.type_selection_id = self.selection_nobody
        warning = relation_nobody.onchange_partner_id()["warning"]
        self.assertTrue("message" in warning)
        self.assertTrue("incompatible" in warning["message"])

    def test_compute_domains(self):
        """Test the function that should set domains on open of form."""
        # Use NGO to volunteer relation.
        relation = self.relation_all_model.search(
            [
                ("this_partner_id", "=", self.partner_ngo_test.id),
                ("type_selection_id", "=", self.selection_ngo_has_volunteer.id),
                ("other_partner_id", "=", self.partner_volunteer_test.id),
            ],
            limit=1,
        )
        relation._compute_domains()  # pylint: disable=protected-access
        # Selection of this_partner_id must be for organisations that
        # are NGO's.
        self.assertIn(
            [u"is_company", u"=", True], json.loads(relation.this_partner_id_domain)
        )
        self.assertIn(
            [u"category_id", u"in", [self.category_ngo.id]],
            json.loads(relation.this_partner_id_domain),
        )
        # Selection of type_selection_id should be limited to types that:
        # a. Have organisations for this partner, or allow all partner types;
        # b. Have a category that is present on this partner, or do not
        #    demand a specific category;
        # c. and d. The same as a. and b. but for other partner (not tested).
        self.assertIn(
            [u"contact_type_this", u"=", False],
            json.loads(relation.type_selection_id_domain),
        )
        self.assertIn(
            [u"contact_type_this", u"=", u"c"],
            json.loads(relation.type_selection_id_domain),
        )
        self.assertIn(
            [u"partner_category_this", u"=", False],
            json.loads(relation.type_selection_id_domain),
        )
        self.assertIn(
            [u"partner_category_this", u"in", self.partner_ngo_test.category_id.ids],
            json.loads(relation.type_selection_id_domain),
        )
        # Selection of other_partner_id must be for persons that
        # are volunteers.
        self.assertIn(
            [u"is_company", u"=", False], json.loads(relation.other_partner_id_domain)
        )
        self.assertIn(
            [u"category_id", u"in", [self.category_volunteer.id]],
            json.loads(relation.other_partner_id_domain),
        )

    def test_write(self):
        """Test write. Special attention for changing type."""
        relation = self.relation_ceo
        company_partner = relation.this_partner_id
        # First get another worker:
        partner_extra_person = self.partner_model.create(
            {"name": "A new worker", "is_company": False, "ref": "NW01"}
        )
        relation.write({"other_partner_id": partner_extra_person.id})
        self.assertEqual(relation.other_partner_id.name, partner_extra_person.name)
        # We will also change to a type going from person to company:
        relation.write(
            {
                "this_partner_id": partner_extra_person.id,
                "type_selection_id": self.selection_person_is_director.id,
                "other_partner_id": company_partner.id,
            }
        )
        self.assertEqual(relation.this_partner_id.id, partner_extra_person.id)
        self.assertEqual(
            relation.type_selection_id.id, self.selection_person_is_director.id
        )
        self.assertEqual(relation.other_partner_id.id, company_partner.id)

    def test_inverse_write(self):
        """Test write of record through inverse selection."""
        # Create record through inverse relation.
        relation = self.relation_all_model.create(
            {
                "this_partner_id": self.partner_bart.id,
                "type_selection_id": self.selection_person_is_employee.id,
                "other_partner_id": self.partner_company_test.id,
            }
        )
        # Now change to not inverse relation type.
        relation.write({"type_selection_id": self.selection_person_is_director.id})
        # Because we switched from inverse to non inverse relation,
        # the this and other partner also switched, as the 'self'
        # is now pointing to the relation from the other side.
        self.assertEqual(relation.this_partner_id, self.partner_company_test)
        self.assertEqual(
            relation.type_selection_id, self.selection_company_has_director
        )
        self.assertEqual(relation.other_partner_id, self.partner_bart)
