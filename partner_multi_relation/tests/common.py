# Copyright 2016-2021 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
"""Common setup for partner_multi_relation test cases."""
from odoo.tests import common


# pylint: disable=too-many-instance-attributes,too-few-public-methods


class PartnerRelationCase(common.TransactionCase):
    """Common setup for partner_multi_relation test cases."""

    # pylint: disable=invalid-name
    def setUp(self):
        """Common setup for partner_multi_relation tests."""
        super().setUp()

        # Models.
        self.partner_model = self.env["res.partner"]
        self.category_model = self.env["res.partner.category"]
        self.type_model = self.env["res.partner.relation.type"]
        self.selection_model = self.env["res.partner.relation.type.selection"]
        self.relation_model = self.env["res.partner.relation"]
        self.relation_all_model = self.env["res.partner.relation.all"]
        # Categories.
        self.category_ngo = self.env.ref("partner_multi_relation.category_ngo")
        self.category_volunteer = self.env.ref(
            "partner_multi_relation.category_volunteer"
        )
        # Partners.
        self.partner_company_test = self.env.ref(
            "partner_multi_relation.partner_company_test"
        )
        self.partner_person_test = self.env.ref(
            "partner_multi_relation.partner_person_test"
        )
        self.partner_ngo_test = self.env.ref("partner_multi_relation.partner_ngo_test")
        self.partner_volunteer_test = self.env.ref(
            "partner_multi_relation.partner_volunteer_test"
        )
        # Relation types.
        # Company has employee.
        self.relation_type_company_has_employee = self.env.ref(
            "partner_multi_relation.relation_type_company_has_employee"
        )
        self.selection_company_has_employee = self._get_selection_type(
            self.relation_type_company_has_employee, is_inverse=False
        )
        self.selection_person_is_employee = self._get_selection_type(
            self.relation_type_company_has_employee, is_inverse=True
        )
        # Person is director of.
        self.relation_type_person_is_director = self.env.ref(
            "partner_multi_relation.relation_type_person_is_director"
        )
        self.selection_person_is_director = self._get_selection_type(
            self.relation_type_person_is_director, is_inverse=False
        )
        self.selection_company_has_director = self._get_selection_type(
            self.relation_type_person_is_director, is_inverse=True
        )
        # NGO has volunteer:
        self.relation_type_ngo_has_volunteer = self.env.ref(
            "partner_multi_relation.relation_type_ngo_has_volunteer"
        )
        self.selection_ngo_has_volunteer = self._get_selection_type(
            self.relation_type_ngo_has_volunteer, is_inverse=False
        )
        self.selection_volunteer_for = self._get_selection_type(
            self.relation_type_ngo_has_volunteer, is_inverse=True
        )
        # Relations.
        self.relation_company2employee = self.env.ref(
            "partner_multi_relation.relation_company2employee"
        )
        self.relation_ngo2volunteer = self.env.ref(
            "partner_multi_relation.relation_ngo2volunteer"
        )

    def _get_selection_type(self, base_type, is_inverse=False):
        selection_id = base_type.id * 2 + (is_inverse and 1 or 0)
        return self.selection_model.browse([selection_id])[0]
