# Copyright 2026 Therp BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import uuid

from odoo.tests import common


class TestCommonCase(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        """Main Set Up Class."""
        super().setUpClass()
        cls.Partner = cls.env["res.partner"]
        cls.RelationType = cls.env["res.partner.relation.type"]
        cls.Relation = cls.env["res.partner.relation"]
        cls.partner_01_person = cls.Partner.create(
            {"name": "Test User 1", "is_company": False, "ref": "PR01"}
        )
        cls.partner_02_company = cls.Partner.create(
            {"name": "Test Company", "is_company": True, "ref": "PR02"}
        )
        cls.type_company2person = cls.RelationType.create(
            {
                "name": "has lawyer",
                "name_inverse": "is lawyer for",
                "contact_type_left": "c",
                "contact_type_right": "p",
                "handle_invalid_onchange": "restrict",
            }
        )
        cls.company2person_relation = cls.Relation.create(
            {
                "left_partner_id": cls.partner_02_company.id,
                "type_id": cls.type_company2person.id,
                "right_partner_id": cls.partner_01_person.id,
            }
        )

    def _action_contact_address(self, relation):
        """Will raise an exception if relation.type_id doesn't allow contact address."""
        action = relation.action_contact_address()
        context = action["context"]
        vals = self.Partner.with_context(**context).default_get(
            fields_list=self.Partner._fields.keys()  # Default for all fields
        )
        self.assertIn("name", vals)
        vals["ref"] = uuid.uuid1()  # We need a unique reference in these tests.
        return self.Partner.create(vals)
