# Copyright 2016 Therp BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestPartnerRelationCommon(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        """Main Set Up Class."""
        super().setUpClass()
        cls.partner_model = cls.env["res.partner"]
        cls.category_model = cls.env["res.partner.category"]
        cls.type_model = cls.env["res.partner.relation.type"]
        cls.selection_model = cls.env["res.partner.relation.type.selection"]
        cls.relation_model = cls.env["res.partner.relation"]
        cls.relation_all_model = cls.env["res.partner.relation.all"]
        cls.partner_01_person = cls.partner_model.create(
            {"name": "Test User 1", "is_company": False, "ref": "PR01"}
        )
        cls.partner_02_company = cls.partner_model.create(
            {"name": "Test Company", "is_company": True, "ref": "PR02"}
        )
        # Create partners with specific categories:
        cls.category_01_ngo = cls.category_model.create({"name": "NGO"})
        cls.partner_03_ngo = cls.partner_model.create(
            {
                "name": "Test NGO",
                "is_company": True,
                "ref": "PR03",
                "category_id": [(4, cls.category_01_ngo.id)],
            }
        )
        cls.category_02_volunteer = cls.category_model.create({"name": "Volunteer"})
        cls.partner_04_volunteer = cls.partner_model.create(
            {
                "name": "Test Volunteer",
                "is_company": False,
                "ref": "PR04",
                "category_id": [(4, cls.category_02_volunteer.id)],
            }
        )
        # Create a new relation type withouth categories:
        (
            cls.type_company2person,
            cls.selection_company2person,
            cls.selection_person2company,
        ) = cls._create_relation_type_selection(
            {
                "name": "mixed",
                "name_inverse": "mixed_inverse",
                "contact_type_left": "c",
                "contact_type_right": "p",
            }
        )
        # Create a new relation type with categories:
        (
            cls.type_ngo2volunteer,
            cls.selection_ngo2volunteer,
            cls.selection_volunteer2ngo,
        ) = cls._create_relation_type_selection(
            {
                "name": "NGO has volunteer",
                "name_inverse": "volunteer works for NGO",
                "contact_type_left": "c",
                "contact_type_right": "p",
                "partner_category_left": cls.category_01_ngo.id,
                "partner_category_right": cls.category_02_volunteer.id,
            }
        )

    @classmethod
    def _create_relation_type_selection(cls, vals):
        """Create relation type and return this with selection types."""
        vals_list = [vals]
        new_type = cls.type_model.create(vals_list)
        selection_types = cls.selection_model.search([("type_id", "=", new_type.id)])
        for st in selection_types:
            if st.is_inverse:
                inverse_type_selection = st
            else:
                type_selection = st
        return (new_type, type_selection, inverse_type_selection)

    @classmethod
    def _create_company2person_relation(cls):
        """Utility function to get a relation from company 2 partner."""
        return cls.relation_all_model.create(
            {
                "type_selection_id": cls.selection_company2person.id,
                "this_partner_id": cls.partner_02_company.id,
                "other_partner_id": cls.partner_01_person.id,
            }
        )
