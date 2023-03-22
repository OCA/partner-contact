from odoo.tests import common


class TestPartnerDeliveryLink(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].create(
            {
                "name": "Test Partner 1",
                "email": "testpartner1@example.org",
                "is_company": True,
                "parent_id": False,
            }
        )
        self.company = self.env.user.company_id
        self.product = self.env["product.product"].create(
            {"name": "Product 2 test", "type": "product"}
        )
        self.carrier = self.env["delivery.carrier"].create(
            {
                "name": "Test Fixed delivery method",
                "product_id": self.product.id,
            }
        )

    def _create_delivery(self):
        picking_type = self.env["stock.picking.type"].search(
            [
                ("code", "=", "outgoing"),
                "|",
                ("warehouse_id.company_id", "=", self.company.id),
                ("warehouse_id", "=", False),
            ],
            limit=1,
        )
        picking_form = common.Form(
            recordp=self.env["stock.picking"].with_context(
                default_picking_type_id=picking_type.id
            ),
            view="stock.view_picking_form",
        )

        picking_form.partner_id = self.partner
        with picking_form.move_ids_without_package.new() as move:
            move.product_id = self.product
            move.product_uom_qty = 10
        picking = picking_form.save()
        self.env["stock.picking.delivery"].create(
            {
                "carrier_id": self.carrier.id,
                "picking_id": picking.id,
                "carrier_tracking_ref": "Tester",
            }
        )
        picking.action_confirm()
        for move in picking.move_lines:
            move.quantity_done = move.product_uom_qty
        picking.button_validate()
        return picking

    def test_delivery_link(self):
        self._create_delivery()
        self.assertEqual(self.partner.partner_delivery_count, 1)
        self.assertTrue(self.partner.action_view_partner_delivery())
