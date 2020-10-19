# Copyright 2020 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Test action methods added to res.partner model."""
from odoo.tools.safe_eval import safe_eval

from .test_partner_relation_common import TestPartnerRelationCommon


class TestPartnerAction(TestPartnerRelationCommon):
    """Test action methods added to res.partner model."""

    def test_action_view_relations(self):
        """Test searching on relation type."""
        relation = self._create_company2person_relation()
        this_partner = relation.this_partner_id
        action = this_partner.action_view_relations()
        # relation should be found by domain from action.
        partner_relations = self.relation_all_model.search(action["domain"])
        self.assertIn(relation, partner_relations)
        # Context should be evaluable and contain this id in active id.
        context = safe_eval(action["context"])
        self.assertEqual(this_partner.id, context["active_id"])
