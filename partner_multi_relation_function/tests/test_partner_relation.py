# Copyright 2026 Therp BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.exceptions import ValidationError
from odoo.tests import common


class TestPartnerRelation(common.TransactionCase):
    def test_allow_function(self):
        Partner = self.env["res.partner"]
        RelationType = self.env["res.partner.relation.type"]
        Relation = self.env["res.partner.relation"]
        partner_person = Partner.create(
            {"name": "Test Participant", "is_company": False, "ref": "PR01"}
        )
        partner_project = Partner.create(
            {"name": "Test Project", "is_company": True, "ref": "PR02"}
        )
        relation_type = RelationType.create(
            {
                "name": "project has participant",
                "name_inverse": "participates in project",
                "contact_type_left": "c",
                "contact_type_right": "p",
                "allow_function": False,
            }
        )
        relation_vals = {
            "left_partner_id": partner_project.id,
            "type_id": relation_type.id,
            "function": "coordinator",
            "right_partner_id": partner_person.id,
        }
        with self.assertRaises(ValidationError):
            # We do not allow a function yet.
            relation_with_function = Relation.create(relation_vals)
        # Now do allow function.
        relation_type.write({"allow_function": True})
        relation_with_function = Relation.create(relation_vals)
        self.assertTrue(relation_with_function)
