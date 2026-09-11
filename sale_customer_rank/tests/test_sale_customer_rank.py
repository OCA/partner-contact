# Copyright 2022 ForgeFlow, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase

from .. import post_init_hook


class TestCustomerRank(TransactionCase):
    def test_customer_rank(self):
        partner = self.env["res.partner"].create({"name": "test partner"})
        self.assertEqual(partner.customer_rank, 0)
        self.env["sale.order"].create({"name": "test sale", "partner_id": partner.id})
        self.assertEqual(partner.customer_rank, 1)

    def test_post_init_hook(self):
        parent_partner = self.env["res.partner"].create(
            {"name": "Parent Company", "is_company": True}
        )
        child_partner = self.env["res.partner"].create(
            {"name": "Child Contact", "parent_id": parent_partner.id}
        )
        self.env["sale.order"].create(
            {"name": "test hook sale", "partner_id": child_partner.id}
        )
        (parent_partner | child_partner).write({"customer_rank": 0})
        post_init_hook(self.env)
        self.assertEqual(child_partner.customer_rank, 1)
        self.assertEqual(parent_partner.customer_rank, 1)
