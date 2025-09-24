# Copyright 2025 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from psycopg2.errors import ForeignKeyViolation

from odoo.exceptions import ValidationError
from odoo.tools.misc import mute_logger

from .test_partner_relation_common import TestPartnerRelationCommon


class TestPartnerRelationType(TestPartnerRelationCommon):
    @mute_logger("odoo.sql_db")
    def test_unlink(self):
        """Unlink should fail if existing relations are not unlinked also."""
        relation_type = self.type_company2person
        relation = self.company2person_relation
        with self.assertRaises(ForeignKeyViolation):
            relation_type.unlink()
        relation_type.write({"handle_invalid_onchange": "delete"})
        self.assertTrue(relation_type.unlink())
        self.assertFalse(relation.exists())

    def test_write_partner_type(self):
        """Create relation company 2 person, then change left type to person."""
        relation_type = self.type_company2person
        relation = self.company2person_relation
        self.assertTrue(relation.left_partner_id.is_company)
        with self.assertRaises(ValidationError):
            relation_type.write({"left_partner_type": "p"})
        # But should be OK if we end the incompatible relations.
        relation_type.write(
            {
                "handle_invalid_onchange": "end",
                "left_partner_type": "p",
            }
        )
        self.assertTrue(relation.date_end)

    def test_write_partner_type_company(self):
        """Create relation company 2 person, then change right type to company."""
        relation_type = self.type_company2person
        relation = self.company2person_relation
        self.assertFalse(relation.right_partner_id.is_company)
        with self.assertRaises(ValidationError):
            relation_type.write({"right_partner_type": "c"})
        # But should be OK if we delete the incompatible relations.
        relation_type.write(
            {
                "handle_invalid_onchange": "delete",
                "right_partner_type": "c",
            }
        )
        self.assertFalse(relation.exists())

    def test_write_remove_partner_types(self):
        """Create relation company 2 person, then make all kind of changes possible."""
        relation_type = self.type_company2person
        relation = self.company2person_relation
        relation_type.write(
            {
                "left_partner_type": False,
                "right_partner_type": False,
            }
        )
        # Now we should be able to add person left and company right.
        self.assertTrue(
            relation.write(
                {
                    "left_partner_id": self.partner_04_volunteer.id,
                    "right_partner_id": self.partner_03_ngo.id,
                }
            )
        )

    def test_write_category(self):
        """Create relation company 2 person, then change left category to ngo."""
        relation_type = self.type_company2person
        relation = self.company2person_relation
        self.assertFalse(relation.left_partner_id.category_id)
        with self.assertRaises(ValidationError):
            relation_type.write({"left_partner_category_id": self.category_01_ngo.id})
        # But should be OK if we ignore the incompatible relations.
        relation_type.write(
            {
                "handle_invalid_onchange": "ignore",
                "left_partner_category_id": self.category_01_ngo.id,
            }
        )
        self.assertFalse(relation.left_partner_id.category_id)

    def test_write_with_no_incompatible_relations(self):
        """Create relation type without conditions, relation, then add conditions."""
        type_party_volunteer = self.RelationType.create(
            {
                "name": "party has volunteer",
                "name_inverse": "volunteer works for party",
                "handle_invalid_onchange": "restrict",
            }
        )
        category_party = self.PartnerCategory.create({"name": "Party"})
        partner_peoples_will = self.Partner.create(
            {
                "name": "People's Will",
                "is_company": True,
                "ref": "PPLWIL",
                "category_id": [(4, category_party.id)],
            }
        )
        self.Relation.create(
            {
                "left_partner_id": partner_peoples_will.id,
                "type_id": type_party_volunteer.id,
                "right_partner_id": self.partner_04_volunteer.id,
            }
        )
        self.assertTrue(
            type_party_volunteer.write(
                {
                    "left_partner_type": "c",
                    "right_partner_type": "p",
                    "left_partner_category_id": category_party.id,
                    "right_partner_category_id": self.category_02_volunteer.id,
                }
            )
        )

    def test_symmetric(self):
        """When making connection symmetric, set right values to left values."""
        relation_type = self.RelationType.create(
            {
                "name": "is related to",
                "name_inverse": "has a relation to",
                "left_partner_type": "p",
                "left_partner_category_id": self.category_01_ngo.id,
            }
        )
        relation_type.write({"is_symmetric": True})
        self.assertTrue(relation_type.is_symmetric)
        self.assertEqual(relation_type.name_inverse, relation_type.name)
        self.assertEqual(
            relation_type.right_partner_type, relation_type.left_partner_type
        )
        self.assertEqual(
            relation_type.right_partner_category_id,
            relation_type.left_partner_category_id,
        )
