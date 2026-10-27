# Copyright 2024 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon


class TestPartnerShippingPolicy(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["res.partner"]
        cls.sale_order_model = cls.env["sale.order"]
        cls.partner = cls.partner_model.create(
            {"name": "Test Partner", "picking_policy": "one"}
        )
        cls.delivery_address = cls.partner_model.create(
            {
                "name": "Test Delivery Address",
                "picking_policy": "direct",
                "type": "delivery",
                "parent_id": cls.partner.id,
            }
        )
        cls.partner_2 = cls.partner_model.create(
            {"name": "Test Partner 2", "picking_policy": ""}
        )
        cls.partner_3 = cls.partner_model.create(
            {"name": "Test Partner 3", "picking_policy": "one"}
        )

        cls.env["ir.config_parameter"].sudo().set_param(
            "sale_stock.default_picking_policy", "direct"
        )

    def test_01_partner_picking_policy(self):
        sale_selection = self.env["sale.order"].fields_get(["picking_policy"])[
            "picking_policy"
        ]["selection"]
        partner_selection = self.env["res.partner"].fields_get(["picking_policy"])[
            "picking_policy"
        ]["selection"]
        self.assertEqual(sale_selection, partner_selection)

    def test_02_partner_picking_policy(self):
        sale_form = Form(self.sale_order_model)
        sale_form.partner_id = self.partner
        self.assertEqual(sale_form.picking_policy, self.delivery_address.picking_policy)
        sale_form.partner_id = self.partner_2
        self.assertEqual(sale_form.picking_policy, "direct")
        sale_form.partner_id = self.partner_3
        self.assertEqual(sale_form.picking_policy, self.partner_3.picking_policy)

    def test_03_create_with_partner(self):
        order = self.sale_order_model.create({"partner_id": self.partner_3.id})
        self.assertEqual(order.picking_policy, "one")

    def test_04_form_with_default_partner(self):
        sale_form = Form(
            self.sale_order_model.with_context(default_partner_id=self.partner_3.id)
        )
        self.assertEqual(sale_form.picking_policy, "one")

    def test_05_create_explicit_value_kept(self):
        order = self.sale_order_model.create(
            {"partner_id": self.partner_3.id, "picking_policy": "direct"}
        )
        self.assertEqual(order.picking_policy, "direct")

    def test_06_create_context_default_kept(self):
        order = self.sale_order_model.with_context(
            default_picking_policy="direct"
        ).create({"partner_id": self.partner_3.id})
        self.assertEqual(order.picking_policy, "direct")

    def test_07_settings_default_without_partner_policy(self):
        self.env["ir.default"].set("sale.order", "picking_policy", "one")
        order = self.sale_order_model.create({"partner_id": self.partner_2.id})
        self.assertEqual(order.picking_policy, "one")

    def test_08_partner_policy_over_settings_default(self):
        self.env["ir.default"].set("sale.order", "picking_policy", "direct")
        order = self.sale_order_model.create({"partner_id": self.partner_3.id})
        self.assertEqual(order.picking_policy, "one")
