# Copyright 2016-2025 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging
from datetime import date, datetime, timedelta

from odoo import fields
from odoo.exceptions import ValidationError

from .test_partner_relation_common import TestPartnerRelationCommon

_logger = logging.getLogger(__name__)


class TestPartnerRelation(TestPartnerRelationCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create a new relation type which will not have valid relations:
        category_nobody = cls.PartnerCategory.create({"name": "Nobody"})
        cls.type_nobody = cls.RelationType.create(
            {
                "name": "has relation with nobody",
                "name_inverse": "nobody has relation with",
                "left_partner_type": "c",
                "right_partner_type": "p",
                "left_partner_category_id": category_nobody.id,
                "right_partner_category_id": category_nobody.id,
            }
        )

    def _get_empty_relation(self):
        """Get empty relation record for onchange tests."""
        # Need English, because we will compare text
        return self.Relation.with_context(lang="en_US").new({})

    def test_default_get(self):
        """Left partner should be in result if current_partner_id in context."""
        result = self.Relation.with_context(
            current_partner_id=self.partner_04_volunteer.id
        ).default_get(fields_list=self.Relation._fields)
        self.assertIn("left_partner_id", result)
        self.assertEqual(result["left_partner_id"], self.partner_04_volunteer.id)

    def test_get_partner_types(self):
        """Partner types should contain at least 'c' and 'p'."""
        partner_types = self.RelationType.get_partner_types()
        type_codes = [ptype[0] for ptype in partner_types]
        self.assertTrue("c" in type_codes)
        self.assertTrue("p" in type_codes)

    def test_create_with_active_id(self):
        """Test creation with left_partner_id from active_id."""
        # Check wether we can create connection from company to person,
        # taking the particular company from the active records:
        relation = self.Relation.with_context(
            active_id=self.partner_02_company.id,
            active_ids=self.partner_02_company.ids,
            active_model="res.partner",
        ).create(
            {
                "type_id": self.type_company2person.id,
                "right_partner_id": self.partner_04_volunteer.id,
            }
        )
        self.assertTrue(relation)
        self.assertEqual(relation.left_partner_id, self.partner_02_company)
        # Partner should have one relation now:
        self.assertEqual(self.partner_04_volunteer.relation_count, 1)

    def test_display_name(self):
        """Test display name"""
        relation = self.company2person_relation
        self.assertEqual(
            relation.display_name,
            f"{relation.left_partner_id.name} {relation.type_id.name} "
            f"{relation.right_partner_id.name}",
        )

    def test_display_name_inverse(self):
        """Test display name when coming from right partner."""
        relation = self.company2person_relation.with_context(
            current_partner_id=self.partner_01_person.id
        )
        self.assertEqual(
            relation.display_name,
            f"{relation.right_partner_id.name}"
            f" {relation.type_id.name_inverse}"
            f" {relation.left_partner_id.name}",
        )

    def test_depends_context_current_partner_id_no_context(self):
        """Display fields that depend on context, without context."""
        relation = self.company2person_relation
        self.assertEqual(relation.this_partner_id, relation.left_partner_id)
        self.assertEqual(relation.type_id_display, relation.type_id.name)
        self.assertEqual(relation.other_partner_id, relation.right_partner_id)

    def test_depends_context_current_partner_id(self):
        """Display fields that depend on context, with context."""
        relation = self.company2person_relation.with_context(
            current_partner_id=self.partner_01_person.id
        )
        self.assertEqual(relation.this_partner_id, relation.right_partner_id)
        self.assertEqual(relation.type_id_display, relation.type_id.name_inverse)
        self.assertEqual(relation.other_partner_id, relation.left_partner_id)

    def test_validate_partner_type(self):
        """Create with wrong partner for type should raise ValidationError."""
        with self.assertRaises(ValidationError):
            self.Relation.create(
                {
                    # Left partner should be a company, but is not.
                    "left_partner_id": self.partner_04_volunteer.id,
                    "type_id": self.type_company2person.id,
                    "right_partner_id": self.partner_01_person.id,
                }
            )

    def test_validate_contact_category(self):
        """Create with partner with missing category should raise ValidationError."""
        with self.assertRaises(ValidationError):
            self.Relation.create(
                {
                    "left_partner_id": self.partner_03_ngo.id,
                    "type_id": self.type_ngo2volunteer.id,
                    # Right partner does not have volunteer category.
                    "right_partner_id": self.partner_01_person.id,
                }
            )

    def test_write_incompatible_dates(self):
        """Test write with date_end before date_start."""
        relation = self.company2person_relation
        with self.assertRaises(ValidationError):
            relation.write({"date_start": "2016-09-01", "date_end": "2016-08-01"})

    def test_validate_overlapping_01(self):
        """Test create overlapping with no start / end dates."""
        relation = self.company2person_relation
        with self.assertRaises(ValidationError):
            # New relation with no start / end should give error
            self.Relation.create(
                {
                    "left_partner_id": relation.left_partner_id.id,
                    "type_id": relation.type_id.id,
                    "right_partner_id": relation.right_partner_id.id,
                }
            )

    def test_validate_overlapping_02(self):
        """Test create overlapping with start / end dates."""
        relation = self.company2person_relation
        # New relation with overlapping start / end should give error
        with self.assertRaises(ValidationError):
            self.Relation.create(
                {
                    "left_partner_id": relation.left_partner_id.id,
                    "type_id": relation.type_id.id,
                    "right_partner_id": relation.right_partner_id.id,
                    "date_start": "2016-08-01",
                    "date_end": "2017-07-30",
                }
            )

    def test_validate_overlapping_03(self):
        """Test create not overlapping."""
        relation = self.company2person_relation
        relation.write(
            {
                "date_start": "2015-09-01",
                "date_end": "2016-08-31",
            }
        )
        relation_another_record = self.Relation.create(
            {
                "left_partner_id": relation.left_partner_id.id,
                "type_id": relation.type_id.id,
                "right_partner_id": relation.right_partner_id.id,
                "date_start": "2016-09-01",
                "date_end": "2017-08-31",
            }
        )
        self.assertTrue(relation_another_record)

    def test_onchange_type_id_empty_relation(self):
        """Test on_change_type_id with empty relation."""
        relation_empty = self._get_empty_relation()
        result = relation_empty._onchange_type_id()
        domain = self._get_domain_from_logged_result(result)
        self.assertFalse("warning" in result)
        self.assertTrue("left_partner_id" in domain)
        self.assertEqual(domain["left_partner_id"], [])
        self.assertTrue("right_partner_id" in domain)
        self.assertEqual(domain["right_partner_id"], [])

    def test_empty_type_id(self):
        """Test type_id_display empty if type_id empty."""
        relation_empty = self._get_empty_relation()
        relation_empty.update(
            {
                "left_partner_id": self.partner_03_ngo.id,
                "right_partner_id": self.partner_01_person.id,
            }
        )
        self.assertFalse(relation_empty.type_id_display)

    def _get_domain_from_logged_result(self, result):
        """Get domain from result, logging it for easy debugging."""
        _logger.info("result: %s", str(result))
        self.assertTrue("domain" in result)
        return result["domain"]

    def test_onchange_type_id_no_criteria(self):
        """Test on_change_type_id for type with no criteria."""
        type_ngo_volunteer = self.RelationType.create(
            {
                "name": "ngo has volunteer",
                "name_inverse": "volunteer works for ngo",
                "handle_invalid_onchange": "restrict",
            }
        )
        relation = self.Relation.create(
            {
                "left_partner_id": self.partner_03_ngo.id,
                "type_id": type_ngo_volunteer.id,
                "right_partner_id": self.partner_04_volunteer.id,
            }
        )
        result = relation._onchange_type_id()
        domain = self._get_domain_from_logged_result(result)
        self.assertEqual(domain["left_partner_id"], [])
        self.assertEqual(domain["right_partner_id"], [])

    def test_onchange_type_id_company2person(self):
        """Test on_change_type_id with company 2 person relation."""
        relation = self.company2person_relation
        result = relation._onchange_type_id()
        domain = self._get_domain_from_logged_result(result)
        self.assertTrue(("is_company", "=", True) in domain["left_partner_id"])
        self.assertTrue(("is_company", "=", False) in domain["right_partner_id"])

    def test_onchange_type_id_needing_categories(self):
        """Test on_change_type_id with relation needing categories."""
        # Take left partner from active_id.
        relation_ngo_volunteer = self.Relation.with_context(
            active_id=self.partner_03_ngo.id
        ).create(
            {
                "type_id": self.type_ngo2volunteer.id,
                "right_partner_id": self.partner_04_volunteer.id,
            }
        )
        result = relation_ngo_volunteer._onchange_type_id()
        domain = self._get_domain_from_logged_result(result)
        self.assertTrue(
            ("category_id", "=", self.category_01_ngo.id) in domain["left_partner_id"]
        )
        self.assertTrue(
            ("category_id", "=", self.category_02_volunteer.id)
            in domain["right_partner_id"]
        )

    def test_search_any_partner(self):
        """Test searching for partner left or right."""
        relation = self.Relation.search(
            [("any_partner_id", "=", self.partner_02_company.id)]
        )
        self.assertEqual(relation.left_partner_id, self.partner_02_company)
        relation = self.Relation.search([("any_partner_id", "like", "User")])
        self.assertEqual(relation.left_partner_id, self.partner_02_company)
        self.assertEqual(relation.right_partner_id, self.partner_01_person)

    def test_onchange_type_id_impossible_combinations(self):
        """Test on_change_type_id with invalid or impossible combinations."""
        relation_nobody = self._get_empty_relation()
        relation_nobody.type_id = self.type_nobody
        warning = relation_nobody._onchange_type_id()["warning"]
        self.assertTrue("message" in warning)
        self.assertTrue("No left partner available" in warning["message"])
        relation_nobody.left_partner_id = self.partner_02_company
        warning = relation_nobody._onchange_type_id()["warning"]
        self.assertTrue("message" in warning)
        self.assertTrue("incompatible" in warning["message"])
        # Allow left partner and check message for other partner:
        self.type_nobody.write({"left_partner_category_id": False})
        warning = relation_nobody._onchange_type_id()["warning"]
        self.assertTrue("message" in warning)
        self.assertTrue("No right partner available" in warning["message"])

    def test_onchange_partner(self):
        """Test on_change_partner_id."""
        # 1. Test call with empty relation
        relation_empty = self._get_empty_relation()
        result = relation_empty._onchange_partner()
        self.assertTrue("domain" in result)
        self.assertFalse("warning" in result)
        self.assertTrue("type_id" in result["domain"])
        self.assertFalse(result["domain"]["type_id"])
        # 2. Test call with company 2 person relation
        relation = self.company2person_relation
        domain = relation._onchange_partner()["domain"]
        self.assertTrue(("left_partner_type", "=", "c") in domain["type_id"])
        # 3. Test with invalid or impossible combinations
        relation_nobody = self._get_empty_relation()
        relation_nobody.left_partner_id = self.partner_02_company
        relation_nobody.type_id = self.type_nobody
        warning = relation_nobody._onchange_partner()["warning"]
        self.assertTrue("message" in warning)
        self.assertTrue("incompatible" in warning["message"])

    def test_write(self):
        """Test write. Special attention for changing type."""
        relation = self.company2person_relation
        company_partner = relation.left_partner_id
        # First get another worker:
        partner_extra_person = self.Partner.create(
            {"name": "A new worker", "is_company": False, "ref": "NW01"}
        )
        relation.write({"right_partner_id": partner_extra_person.id})
        self.assertEqual(relation.right_partner_id.name, partner_extra_person.name)
        # We will also change to a type going from person to company:
        type_worker2company = self.RelationType.create(
            {
                "name": "works for",
                "name_inverse": "has worker",
                "left_partner_type": "p",
                "right_partner_type": "c",
            }
        )
        relation.write(
            {
                "left_partner_id": partner_extra_person.id,
                "type_id": type_worker2company.id,
                "right_partner_id": company_partner.id,
            }
        )
        self.assertEqual(relation.left_partner_id.id, partner_extra_person.id)
        self.assertEqual(relation.type_id.id, type_worker2company.id)
        self.assertEqual(relation.right_partner_id.id, company_partner.id)

    def test_self_allowed(self):
        """Test creation of relation to same partner when type allows."""
        type_allow = self.RelationType.create(
            {
                "name": "allow",
                "name_inverse": "allow_inverse",
                "left_partner_type": "p",
                "right_partner_type": "p",
                "allow_self": True,
            }
        )
        self.assertTrue(type_allow)
        reflexive_relation = self.Relation.create(
            {
                "type_id": type_allow.id,
                "left_partner_id": self.partner_01_person.id,
                "right_partner_id": self.partner_01_person.id,
            }
        )
        self.assertTrue(reflexive_relation)

    def test_self_disallowed(self):
        """Test creating relation to same partner when disallowed.

        Attempt to create a relation of a partner to the same partner should
        raise an error when the type of relation explicitly disallows this.
        """
        type_disallow = self.RelationType.create(
            {
                "name": "disallow",
                "name_inverse": "disallow_inverse",
                "left_partner_type": "p",
                "right_partner_type": "p",
                "allow_self": False,
            }
        )
        self.assertTrue(type_disallow)
        with self.assertRaises(ValidationError):
            self.Relation.create(
                {
                    "type_id": type_disallow.id,
                    "left_partner_id": self.partner_01_person.id,
                    "right_partner_id": self.partner_01_person.id,
                }
            )

    def test_self_disallowed_after_self_relation_created(self):
        """Test that allow_self can not be true if a reflexive relation already exists.

        If at least one reflexive relation exists for the given type,
        reflexivity can not be disallowed.
        """
        type_allow = self.RelationType.create(
            {
                "name": "allow",
                "name_inverse": "allow_inverse",
                "left_partner_type": "p",
                "right_partner_type": "p",
                "allow_self": True,
            }
        )
        self.assertTrue(type_allow)
        reflexive_relation = self.Relation.create(
            {
                "type_id": type_allow.id,
                "left_partner_id": self.partner_01_person.id,
                "right_partner_id": self.partner_01_person.id,
            }
        )
        self.assertTrue(reflexive_relation)
        with self.assertRaises(ValidationError):
            type_allow.allow_self = False
        # If we remove the reflexive relation, we should be able to change.
        reflexive_relation.unlink()
        type_allow.allow_self = False

    def test_self_disallowed_with_delete_invalid_relations(self):
        """Test handle_invalid_onchange delete with allow_self disabled.

        When deactivating allow_self, if handle_invalid_onchange is set
        to delete, then existing reflexive relations are deleted.

        Non reflexive relations are not modified.
        """
        type_allow = self.RelationType.create(
            {
                "name": "allow",
                "name_inverse": "allow_inverse",
                "left_partner_type": "p",
                "right_partner_type": "p",
                "allow_self": True,
                "handle_invalid_onchange": "delete",
            }
        )
        reflexive_relation = self.Relation.create(
            {
                "type_id": type_allow.id,
                "left_partner_id": self.partner_01_person.id,
                "right_partner_id": self.partner_01_person.id,
            }
        )
        normal_relation = self.Relation.create(
            {
                "type_id": type_allow.id,
                "left_partner_id": self.partner_01_person.id,
                "right_partner_id": self.partner_04_volunteer.id,
            }
        )
        type_allow.allow_self = False
        self.assertFalse(reflexive_relation.exists())
        self.assertTrue(normal_relation.exists())

    def test_self_disallowed_with_end_invalid_relations(self):
        """Test handle_invalid_onchange delete with allow_self disabled.

        When deactivating allow_self, if handle_invalid_onchange is set
        to end, then active reflexive relations are ended.

        Non reflexive relations are not modified.

        Reflexive relations with an end date prior to the current date
        are not modified.
        """
        type_allow = self.RelationType.create(
            {
                "name": "allow",
                "name_inverse": "allow_inverse",
                "left_partner_type": "p",
                "right_partner_type": "p",
                "allow_self": True,
                "handle_invalid_onchange": "end",
            }
        )
        reflexive_relation = self.Relation.create(
            {
                "type_id": type_allow.id,
                "left_partner_id": self.partner_01_person.id,
                "right_partner_id": self.partner_01_person.id,
                "date_start": "2000-01-02",
            }
        )
        past_reflexive_relation = self.Relation.create(
            {
                "type_id": type_allow.id,
                "left_partner_id": self.partner_01_person.id,
                "right_partner_id": self.partner_01_person.id,
                "date_end": "2000-01-01",
            }
        )
        normal_relation = self.Relation.create(
            {
                "type_id": type_allow.id,
                "left_partner_id": self.partner_01_person.id,
                "right_partner_id": self.partner_04_volunteer.id,
            }
        )
        type_allow.allow_self = False
        self.assertEqual(reflexive_relation.date_end, fields.Date.today())
        self.assertEqual(past_reflexive_relation.date_end, date(2000, 1, 1))
        self.assertFalse(normal_relation.date_end)

    def test_self_disallowed_with_future_reflexive_relation(self):
        """Test future reflexive relations are deleted.

        If handle_invalid_onchange is set to end, then deactivating
        reflexivity will delete invalid relations in the future.
        """
        type_allow = self.RelationType.create(
            {
                "name": "allow",
                "name_inverse": "allow_inverse",
                "left_partner_type": "p",
                "right_partner_type": "p",
                "allow_self": True,
                "handle_invalid_onchange": "end",
            }
        )
        future_reflexive_relation = self.Relation.create(
            {
                "type_id": type_allow.id,
                "left_partner_id": self.partner_01_person.id,
                "right_partner_id": self.partner_01_person.id,
                "date_start": datetime.now() + timedelta(1),
            }
        )
        type_allow.allow_self = False
        self.assertFalse(future_reflexive_relation.exists())

    def test_self_default(self):
        """Test default not to allow relation with same partner.

        Attempt to create a relation of a partner to the same partner
        raise an error when the type of relation does not explicitly allow
        this.
        """
        type_default = self.RelationType.create(
            {
                "name": "default",
                "name_inverse": "default_inverse",
                "left_partner_type": "p",
                "right_partner_type": "p",
            }
        )
        self.assertTrue(type_default)
        with self.assertRaises(ValidationError):
            self.Relation.create(
                {
                    "type_id": type_default.id,
                    "left_partner_id": self.partner_01_person.id,
                    "right_partner_id": self.partner_01_person.id,
                }
            )
