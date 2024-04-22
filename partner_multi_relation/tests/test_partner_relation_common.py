# Copyright 2016 Therp BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestPartnerRelationCommon(common.TransactionCase):
    def setUp(self):
        super().setUp()

        self.partner_model = self.env["res.partner"]
        self.category_model = self.env["res.partner.category"]
        self.type_model = self.env["res.partner.relation.type"]
        self.selection_model = self.env["res.partner.relation.type.selection"]
        self.relation_model = self.env["res.partner.relation"]
        self.relation_all_model = self.env["res.partner.relation.all"]
        self.partner_01_person = self.partner_model.create(
            {"name": "Test User 1", "is_company": False, "ref": "PR01"}
        )
        self.partner_02_company = self.partner_model.create(
            {"name": "Test Company", "is_company": True, "ref": "PR02"}
        )
        # Create partners with specific categories:
        self.category_01_ngo = self.category_model.create({"name": "NGO"})
        self.partner_03_ngo = self.partner_model.create(
            {
                "name": "Test NGO",
                "is_company": True,
                "ref": "PR03",
                "category_id": [(4, self.category_01_ngo.id)],
            }
        )
        self.category_02_volunteer = self.category_model.create({"name": "Volunteer"})
        self.partner_04_volunteer = self.partner_model.create(
            {
                "name": "Test Volunteer",
                "is_company": False,
                "ref": "PR04",
                "category_id": [(4, self.category_02_volunteer.id)],
            }
        )
        # Create a new relation type withouth categories:
        (
            self.type_company2person,
            self.selection_company2person,
            self.selection_person2company,
        ) = self._create_relation_type_selection(
            {
                "name": "mixed",
                "name_inverse": "mixed_inverse",
                "contact_type_left": "c",
                "contact_type_right": "p",
            }
        )
        # Create a new relation type with categories:
        (
            self.type_ngo2volunteer,
            self.selection_ngo2volunteer,
            self.selection_volunteer2ngo,
        ) = self._create_relation_type_selection(
            {
                "name": "NGO has volunteer",
                "name_inverse": "volunteer works for NGO",
                "contact_type_left": "c",
                "contact_type_right": "p",
                "partner_category_left": self.category_01_ngo.id,
                "partner_category_right": self.category_02_volunteer.id,
            }
        )

    def _create_relation_type_selection(self, vals):
        """Create relation type and return this with selection types."""
        assert "name" in vals, (
            "Name missing in vals to create relation type. Vals: %s." % vals
        )
        assert "name" in vals, (
            "Name_inverse missing in vals to create relation type. Vals: %s." % vals
        )
        vals_list = [vals]
        new_type = self.type_model.create(vals_list)
        self.assertTrue(new_type, msg="No relation type created with vals %s." % vals)
        selection_types = self.selection_model.search([("type_id", "=", new_type.id)])
        for st in selection_types:
            if st.is_inverse:
                inverse_type_selection = st
            else:
                type_selection = st
        self.assertTrue(
            inverse_type_selection,
            msg="Failed to find inverse type selection based on"
            " relation type created with vals %s." % vals,
        )
        self.assertTrue(
            type_selection,
            msg="Failed to find type selection based on"
            " relation type created with vals %s." % vals,
        )
        return (new_type, type_selection, inverse_type_selection)

    def _create_company2person_relation(self):
        """Utility function to get a relation from company 2 partner."""
        return self.relation_all_model.create(
            {
                "type_selection_id": self.selection_company2person.id,
                "this_partner_id": self.partner_02_company.id,
                "other_partner_id": self.partner_01_person.id,
            }
        )
