from datetime import date, timedelta

from odoo.exceptions import UserError
from odoo.tests import common


class TestPartnerIdentificationStock(common.TransactionCase):
    def setUp(self):
        super(TestPartnerIdentificationStock, self).setUp()
        self.product_obj = self.env["product.product"]
        self.res_partner_id_category_obj = self.env["res.partner.id_category"]
        self.picking_obj = self.env["stock.picking"]
        self.partner_id_category_1 = self.res_partner_id_category_obj.create(
            {"code": "1010", "name": "cat1"}
        )
        self.partner_id_category_2 = self.res_partner_id_category_obj.create(
            {"code": "1011", "name": "cat2"}
        )
        self.partner_id_category_3 = self.res_partner_id_category_obj.create(
            {"code": "1011", "name": "cat3"}
        )
        self.partner_1 = self.env.ref("base.res_partner_1").with_context(
            id_no_validate=True
        )
        self.location_id = self.env.ref("stock.picking_type_out")
        self.partner_2 = self.env.ref("base.res_partner_address_15").with_context(
            id_no_validate=True
        )
        self.category_all = self.env.ref("product.product_category_all")
        self.category_all.write(
            {"require_id_stock_ids": [(6, 0, [self.partner_id_category_1.id])]}
        )
        self.partner_1.write(
            {
                "id_numbers": [
                    (
                        0,
                        0,
                        {
                            "name": "Test Number 1",
                            "category_id": self.partner_id_category_1.id,
                            "valid_until": date.today() + timedelta(days=10),
                            "status": "open",
                        },
                    )
                ]
            }
        )
        self.partner_2.write(
            {
                "id_numbers": [
                    (
                        0,
                        0,
                        {
                            "name": "Test Number 1",
                            "category_id": self.partner_id_category_1.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "Test Number 2",
                            "category_id": self.partner_id_category_2.id,
                        },
                    ),
                ]
            }
        )
        self.product = self.product_obj.create(
            {
                "name": "test_product",
                "require_id_stock_ids": [(6, 0, [self.partner_id_category_1.id])],
            }
        )
        self.stock_location = self.env.ref("stock.stock_location_stock")
        self.warehouse = self.env["stock.warehouse"].search(
            [("lot_stock_id", "=", self.stock_location.id)], limit=1
        )
        self.warehouse.write({"delivery_steps": "pick_pack_ship"})
        self.customer_location = self.env.ref("stock.stock_location_customers")
        self.ship_location = self.warehouse.wh_output_stock_loc_id

    def test_partneridentificationsale(self):

        picking = self.picking_obj.create(
            {
                "partner_id": self.partner_1.id,
                "picking_type_id": self.location_id.id,
                "location_id": self.ship_location.id,
                "location_dest_id": self.customer_location.id,
                "move_line_ids_without_package": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom_id": self.product.uom_id.id,
                            "location_id": self.ship_location.id,
                            "location_dest_id": self.customer_location.id,
                            "product_uom_qty": 2,
                        },
                    )
                ],
            }
        )
        picking.action_confirm()
        picking._compute_id_requirement()
        picking.action_confirm()
        self.partner_1.write(
            {
                "id_numbers": [
                    (
                        0,
                        0,
                        {
                            "name": "Test Number 2",
                            "category_id": self.partner_id_category_1.id,
                        },
                    )
                ]
            }
        )
        picking.write({"partner_id": self.partner_2.id})
        picking._compute_id_requirement()
        with self.assertRaises(UserError):
            picking.action_confirm()
        self.product.product_tmpl_id._onchange_categ_id_require_id_stock_ids()
        self.assertEqual(
            len(self.product.require_id_stock_ids),
            len(self.product.categ_id.require_id_stock_ids),
        )
