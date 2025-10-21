# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from dateutil.relativedelta import relativedelta

from odoo import Command, fields
from odoo.tests import common, tagged


@tagged("res_partner")
class TestPartnerRankCommercialEntity(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.Partner = self.env["res.partner"].with_context(no_state_required=True)
        self.Product = self.env["product.product"]
        self.customer = self.Partner.create(
            {
                "name": "Customer",
                "is_company": True,
            }
        )
        self.supplier = self.Partner.create(
            {
                "name": "Supplier",
                "is_company": True,
            }
        )
        self.table = self.Product.create({"name": "Table"})

    def _create_invoice(self, move_type, date, partner_id, **kwargs):
        move = self.env["account.move"].create(
            {
                "invoice_date": date,
                "partner_id": partner_id.id,
                **kwargs,
                "move_type": move_type,
                "date": date,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": self.table.id,
                            "price_unit": 120.0,
                            "tax_ids": [],
                            **line_kwargs,
                        }
                    )
                    for line_kwargs in kwargs.get("invoice_line_ids", [{}])
                ],
            }
        )
        return move.action_post()

    def _check_children_ranks(self, parent_id, field):
        child_ids = self.Partner.search([("parent_id", "=", parent_id.id)])
        if not child_ids:
            return
        parent_rank = getattr(parent_id, field)
        self.assertTrue(
            all(getattr(child, field) == parent_rank for child in child_ids)
        )

    def _propagate_ranks(self, move_type, parent_id, rank_field):
        today = fields.Date.today()

        # New child partner should have the same rank after the first move
        self.Partner.create({"name": "Contact A", "parent_id": parent_id.id})
        self._create_invoice(move_type=move_type, date=today, partner_id=parent_id)
        self.assertEqual(getattr(parent_id, rank_field), 1)
        self._check_children_ranks(parent_id, rank_field)

        # New move increases rank; all existing children have the updated rank
        self._create_invoice(
            move_type=move_type,
            date=today + relativedelta(days=7),
            partner_id=parent_id,
        )
        self.assertEqual(getattr(parent_id, rank_field), 2)
        self._check_children_ranks(parent_id, rank_field)

        # Child partner created after rank increase should have the updated rank
        self.Partner.create({"name": "Contact B", "parent_id": parent_id.id})
        self._check_children_ranks(parent_id, rank_field)

    def test_00_customer_rank_propagation_to_children(self):
        self._propagate_ranks(
            move_type="out_invoice",
            parent_id=self.customer,
            rank_field="customer_rank",
        )

    def test_01_supplier_rank_propagation_to_children(self):
        self._propagate_ranks(
            move_type="in_invoice",
            parent_id=self.supplier,
            rank_field="supplier_rank",
        )
