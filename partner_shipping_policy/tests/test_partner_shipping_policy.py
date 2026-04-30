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
        self.assertEqual(
            sale_form.picking_policy,
            self.env["sale.order"]
            .default_get(["picking_policy"])
            .get("picking_policy"),
        )
        sale_form.partner_id = self.partner_3
        self.assertEqual(sale_form.picking_policy, self.partner_3.picking_policy)

    def test_03_default_get_picking_policy(self):
        # Test when default_partner_id is in context
        res_default_partner = self.sale_order_model.with_context(
            default_partner_id=self.partner.id
        ).default_get(["picking_policy"])
        self.assertEqual(res_default_partner.get("picking_policy"), "one")

        # Test when active_id is in context
        res_active_id = self.sale_order_model.with_context(
            active_id=self.partner.id
        ).default_get(["picking_policy"])
        self.assertEqual(res_active_id.get("picking_policy"), "one")

        # Test when partner has no picking policy (falls back to default)
        res_no_policy = self.sale_order_model.with_context(
            default_partner_id=self.partner_2.id
        ).default_get(["picking_policy"])
        self.assertEqual(res_no_policy.get("picking_policy"), "direct")

        # Test when default_picking_policy is explicitly in context
        res_explicit = self.sale_order_model.with_context(
            default_partner_id=self.partner.id, default_picking_policy="direct"
        ).default_get(["picking_policy"])
        self.assertEqual(res_explicit.get("picking_policy"), "direct")

        # Test when picking_policy is not requested in fields_list
        res_no_field = self.sale_order_model.with_context(
            default_partner_id=self.partner.id
        ).default_get(["name"])
        self.assertNotIn("picking_policy", res_no_field)
