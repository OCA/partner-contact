# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestPartnerAlias(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "search_alias": "alias",
            }
        )

    def test_name_search_with_alias(self):
        partner_ids = self.env["res.partner"]._name_search("alias")
        # Ensure the search returns the created partner
        self.assertIn(
            self.partner.id,
            partner_ids,
            "The partner with search_alias 'alias' should be found.",
        )
