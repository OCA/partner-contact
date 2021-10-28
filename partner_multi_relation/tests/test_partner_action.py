# Copyright 2020-2021 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
"""Test action methods added to res.partner model."""
from odoo.tools.safe_eval import safe_eval

from .common import PartnerRelationCase


# pylint: disable=too-many-instance-attributes,too-few-public-methods


class TestPartnerAction(PartnerRelationCase):
    """Test action methods added to res.partner model."""

    def test_action_view_relations(self):
        """Test searching on relation type."""
        relation = self.relation_company2employee
        company_partner = relation.left_partner_id
        person_partner = relation.right_partner_id
        action = company_partner.action_view_relations()
        # Person should be related to company.
        partner_relations = self.relation_all_model.search(action["domain"])
        self.assertIn(person_partner, partner_relations.mapped("other_partner_id"))
        # Context should be evaluable and contain this id in active id.
        context = safe_eval(action["context"])
        self.assertEqual(company_partner.id, context["active_id"])
