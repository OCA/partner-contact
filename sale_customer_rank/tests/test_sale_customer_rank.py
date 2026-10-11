# Copyright 2022 ForgeFlow, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class TestCustomerRank(TransactionCase):
    def test_customer_rank(self):
        partner = self.env["res.partner"].create({"name": "test partner"})
        self.assertEqual(partner.customer_rank, 0)
        self.env["sale.order"].create({"name": "test sale", "partner_id": partner.id})
        self.assertEqual(partner.customer_rank, 1)
