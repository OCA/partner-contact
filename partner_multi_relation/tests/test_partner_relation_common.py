# Copyright 2016-2025 Therp BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestPartnerRelationCommon(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        """Main Set Up Class."""
        super().setUpClass()
        cls.Partner = cls.env["res.partner"]
        cls.PartnerCategory = cls.env["res.partner.category"]
        cls.RelationType = cls.env["res.partner.relation.type"]
        cls.Relation = cls.env["res.partner.relation"]
        cls.partner_01_person = cls.Partner.create(
            {"name": "Test User 1", "is_company": False, "ref": "PR01"}
        )
        cls.partner_02_company = cls.Partner.create(
            {"name": "Test Company", "is_company": True, "ref": "PR02"}
        )
        # Create partners with specific categories:
        cls.category_01_ngo = cls.PartnerCategory.create({"name": "NGO"})
        cls.partner_03_ngo = cls.Partner.create(
            {
                "name": "Test NGO",
                "is_company": True,
                "ref": "PR03",
                "category_id": [(4, cls.category_01_ngo.id)],
            }
        )
        cls.category_02_volunteer = cls.PartnerCategory.create({"name": "Volunteer"})
        cls.partner_04_volunteer = cls.Partner.create(
            {
                "name": "Test Volunteer",
                "is_company": False,
                "ref": "PR04",
                "category_id": [(4, cls.category_02_volunteer.id)],
            }
        )
        # Create a new relation type withouth categories:
        cls.type_company2person = cls.RelationType.create(
            {
                "name": "has contact",
                "name_inverse": "is contact for",
                "left_partner_type": "c",
                "right_partner_type": "p",
                "handle_invalid_onchange": "restrict",
            }
        )
        # Create a new relation type with categories:
        cls.type_ngo2volunteer = cls.RelationType.create(
            {
                "name": "NGO has volunteer",
                "name_inverse": "volunteer works for NGO",
                "left_partner_type": "c",
                "right_partner_type": "p",
                "left_partner_category_id": cls.category_01_ngo.id,
                "right_partner_category_id": cls.category_02_volunteer.id,
            }
        )
        cls.company2person_relation = cls.Relation.create(
            {
                "left_partner_id": cls.partner_02_company.id,
                "type_id": cls.type_company2person.id,
                "right_partner_id": cls.partner_01_person.id,
            }
        )
