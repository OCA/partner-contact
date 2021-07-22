from datetime import date, timedelta

from odoo.exceptions import UserError
from odoo.tests import common


class TestPartnerIdentificationSale(common.TransactionCase):
    def setUp(self):
        super(TestPartnerIdentificationSale, self).setUp()
        self.product_obj = self.env["product.product"]
        self.res_partner_id_category_obj = self.env["res.partner.id_category"]
        self.sale_obj = self.env["sale.order"]
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
        self.partner_2 = self.env.ref("base.res_partner_address_15").with_context(
            id_no_validate=True
        )
        self.category_all = self.env.ref("product.product_category_all")
        self.category_all.write(
            {"require_id_sale_ids": [(6, 0, [self.partner_id_category_1.id])]}
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
        self.product_desk = self.product_obj.create(
            {
                "name": "Desk",
            }
        )

        self.product_cabinet = self.product_obj.create(
            {
                "name": "Cabinet",
                "require_id_sale_ids": [(4, self.partner_id_category_1.id)],
            }
        )
        self.product = self.product_obj.create(
            {
                "name": "test_product",
                "require_id_sale_ids": [(6, 0, [self.partner_id_category_1.id])],
            }
        )

    def test_partneridentificationsale(self):

        sale_order = self.sale_obj.create(
            {
                "partner_id": self.partner_1.id,
                "partner_invoice_id": self.partner_1.id,
                "partner_shipping_id": self.partner_1.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 2,
                        },
                    )
                ],
            }
        )
        sale_order._compute_id_requirement()
        sale_order.write({"state": "sent"})
        sale_order._compute_id_requirement()
        sale_order.action_confirm()
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
        sale_order.write({"partner_id": self.partner_2.id})
        sale_order._compute_id_requirement()
        sale_order.action_confirm()

        sale_order_two = self.sale_obj.create(
            {
                "partner_id": self.partner_1.id,
                "partner_invoice_id": self.partner_1.id,
                "partner_shipping_id": self.partner_1.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_desk.id,
                            "product_uom_qty": 2,
                        },
                    )
                ],
            }
        )
        sale_order_two.write({"state": "sent"})
        sale_order_two._compute_id_requirement()
        sale_order_three = self.sale_obj.create(
            {
                "partner_id": self.partner_2.id,
                "partner_invoice_id": self.partner_2.id,
                "partner_shipping_id": self.partner_2.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_cabinet.id,
                            "product_uom_qty": 2,
                        },
                    )
                ],
            }
        )
        sale_order_three.write({"state": "sent"})
        sale_order_three._compute_id_requirement()
        with self.assertRaises(UserError):
            sale_order_three.action_confirm()

        self.product.product_tmpl_id._onchange_categ_id_require_id_sale_ids()
