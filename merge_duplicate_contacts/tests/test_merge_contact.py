import odoo.tests.common as common


class TestPartnerMerge(common.SingleTransactionCase):
    def test_merge_contact(self):
        partner_pool = self.env["res.partner"]
        self.partner1 = partner_pool.create(
            {
                "name": "test1",
                "email": "test@example.com",
                "phone": 987654,
            }
        )
        partner_pool |= self.partner1
        self.partner2 = partner_pool.create(
            {
                "name": "test1 (copy)",
                "email": "test@example.com",
                "phone": 987654,
            }
        )
        partner_pool |= self.partner2
        wiz_act = partner_pool.open_wizard_action()
        merge_wizard = (
            self.env[wiz_act["res_model"]]
            .with_context(**wiz_act["context"])
            .create({"keep2": True, "keep1": False})
        )
        merge_wizard._onchange_keep2()
        merge_wizard.action_merge()
        partner_id = self.env["res.partner"].browse(self.partner2.id).exists()
        self.assertTrue(partner_id)
        self.assertEqual(self.partner2.id, merge_wizard.dst_partner_id.id)

    def test_merge_partner_swap(self):
        partner_pool = self.env["res.partner"]
        self.partner1 = partner_pool.create(
            {
                "name": "test1",
                "email": "test@example.com",
                "phone": 987654,
                "vat": "BE0477472702",
            }
        )
        partner_pool |= self.partner1
        self.partner2 = partner_pool.sudo().create(
            {
                "name": "test1 (copy)",
                "email": "test@example.com",
                "phone": 987654321,
                "company_id": self.env.user.company_id.id,
            }
        )
        partner_pool |= self.partner2
        proudct_id = self.env["product.product"].create(
            {
                "name": "test product A",
                "standard_price": 160,
                "list_price": 180,
                "type": "consu",
                "invoice_policy": "order",
                "expense_policy": "cost",
                "default_code": "PROD_COST",
                "service_type": "manual",
            }
        )
        sale_order = (
            self.env["sale.order"]
            .with_context(mail_notrack=True, mail_create_nolog=True)
            .create(
                {
                    "partner_id": self.partner2.id,
                    "partner_invoice_id": self.partner2.id,
                    "partner_shipping_id": self.partner2.id,
                    "order_line": [
                        (
                            0,
                            0,
                            {
                                "name": "test product A",
                                "product_id": proudct_id.id,
                                "product_uom_qty": 2,
                                "qty_delivered": 1,
                            },
                        )
                    ],
                }
            )
        )
        for line in sale_order.order_line:
            line.product_id_change()

        sale_order.onchange_partner_id()
        sale_order._compute_tax_id()
        sale_order.action_confirm()

        self.partner2.with_context(**{"only_show_customer_id": True}).name_get()
        self.partner1.with_context(**{"only_show_customer_id": True}).name_get()
        wiz_act = partner_pool.open_wizard_action()
        partner_name = self.partner2.name
        partner_phone = self.partner1.phone
        merge_wizard = (
            self.env[wiz_act["res_model"]]
            .with_context(**wiz_act["context"])
            .create({"keep2": False, "keep1": True})
        )
        merge_wizard._onchange_keep1()
        merge_wizard.with_context(
            **{
                "field_name": "name",
            }
        ).swap_to_right()
        merge_wizard.with_context(
            **{
                "field_name": "phone2",
            }
        ).swap_to_left()
        merge_wizard.action_merge()
        partner_id = self.env["res.partner"].browse(self.partner2.id).exists()
        self.assertTrue(partner_id)
        self.assertEqual(partner_phone, merge_wizard.dst_partner_id.phone)
        self.assertEqual(partner_name, merge_wizard.dst_partner_id.name)
        self.assertEqual(self.partner2.id, merge_wizard.dst_partner_id.id)

    def test_merge_partner_right_swap_records(self):
        partner_pool = self.env["res.partner"]
        self.partner1 = partner_pool.create(
            {
                "name": "test1",
                "email": "test@example.com",
                "phone": 987654,
                "vat": "BE0477472702",
            }
        )
        partner_pool |= self.partner1
        self.partner2 = partner_pool.sudo().create(
            {
                "name": "test1 (copy)",
                "email": "test@example.com",
                "phone": 987654321,
                "company_id": self.env.user.company_id.id,
            }
        )
        partner_pool |= self.partner2
        proudct_id = self.env["product.product"].create(
            {
                "name": "test product A",
                "standard_price": 160,
                "list_price": 180,
                "type": "consu",
                "invoice_policy": "order",
                "expense_policy": "cost",
                "default_code": "PROD_COST",
                "service_type": "manual",
            }
        )
        sale_order = (
            self.env["sale.order"]
            .with_context(mail_notrack=True, mail_create_nolog=True)
            .create(
                {
                    "partner_id": self.partner2.id,
                    "partner_invoice_id": self.partner2.id,
                    "partner_shipping_id": self.partner2.id,
                    "order_line": [
                        (
                            0,
                            0,
                            {
                                "name": "test product A",
                                "product_id": proudct_id.id,
                                "product_uom_qty": 2,
                                "qty_delivered": 1,
                            },
                        )
                    ],
                }
            )
        )
        for line in sale_order.order_line:
            line.product_id_change()

        sale_order.onchange_partner_id()
        sale_order._compute_tax_id()
        sale_order.action_confirm()

        self.partner2.with_context(**{"only_show_customer_id": True}).name_get()
        self.partner1.with_context(**{"only_show_customer_id": True}).name_get()
        wiz_act = partner_pool.open_wizard_action()
        partner_name = self.partner2.name
        partner_phone = self.partner1.phone
        merge_wizard = (
            self.env[wiz_act["res_model"]]
            .with_context(**wiz_act["context"])
            .create(
                {
                    "keep2": False,
                    "keep1": True,
                    "company_id": self.env.user.company_id.id,
                    "company_name": "Test Abc",
                    "phone": "987654",
                    "mobile": "+156778978",
                    "street": "test street",
                    "street11": "test street 11",
                    "street22": "test street 22",
                    "zip": "202222",
                    "city": "test city",
                    "state_id": 1,
                    "country_id": 2,
                    "is_company": True,
                }
            )
        )
        merge_wizard._onchange_keep1()
        merge_wizard.with_context(
            **{
                "field_name": "name",
            }
        ).swap_to_right()
        merge_wizard.with_context(
            **{
                "field_name": "company_id",
            }
        ).swap_to_right()
        merge_wizard.with_context(
            **{
                "field_name": "company_name",
            }
        ).swap_to_right()
        merge_wizard.with_context(
            **{
                "field_name": "phone",
            }
        ).swap_to_right()
        merge_wizard.with_context(
            **{
                "field_name": "mobile",
            }
        ).swap_to_right()
        merge_wizard.with_context(
            **{
                "field_name": "street",
            }
        ).swap_to_right()
        merge_wizard.with_context(
            **{
                "field_name": "street11",
            }
        ).swap_to_right()
        merge_wizard.with_context(
            **{
                "field_name": "zip",
            }
        ).swap_to_right()
        merge_wizard.with_context(
            **{
                "field_name": "city",
            }
        ).swap_to_right()
        merge_wizard.with_context(
            **{
                "field_name": "state_id",
            }
        ).swap_to_right()
        merge_wizard.with_context(
            **{
                "field_name": "country_id",
            }
        ).swap_to_right()
        merge_wizard.with_context(
            **{
                "field_name": "is_company",
            }
        ).swap_to_right()
        # Ends gere
        merge_wizard.sudo().action_merge()
        partner_id = self.env["res.partner"].browse(self.partner2.id).exists()
        self.assertTrue(partner_id)
        self.assertEqual(partner_phone, merge_wizard.dst_partner_id.phone)
        self.assertEqual(partner_name, merge_wizard.dst_partner_id.name)
        self.assertEqual(self.partner2.id, merge_wizard.dst_partner_id.id)

    def test_merge_partner_left_swap_records(self):
        partner_pool = self.env["res.partner"]
        self.partner1 = partner_pool.create(
            {
                "name": "test1",
                "email": "test@example.com",
                "phone": 987654,
                "vat": "BE0477472702",
            }
        )
        partner_pool |= self.partner1
        self.partner2 = partner_pool.sudo().create(
            {
                "name": "test1 (copy)",
                "email": "test@example.com",
                "phone": 987654321,
                "company_id": self.env.user.company_id.id,
            }
        )
        partner_pool |= self.partner2
        proudct_id = self.env["product.product"].create(
            {
                "name": "test product A",
                "standard_price": 160,
                "list_price": 180,
                "type": "consu",
                "invoice_policy": "order",
                "expense_policy": "cost",
                "default_code": "PROD_COST",
                "service_type": "manual",
            }
        )
        sale_order = (
            self.env["sale.order"]
            .with_context(mail_notrack=True, mail_create_nolog=True)
            .create(
                {
                    "partner_id": self.partner2.id,
                    "partner_invoice_id": self.partner2.id,
                    "partner_shipping_id": self.partner2.id,
                    "order_line": [
                        (
                            0,
                            0,
                            {
                                "name": "test product A",
                                "product_id": proudct_id.id,
                                "product_uom_qty": 2,
                                "qty_delivered": 1,
                            },
                        )
                    ],
                }
            )
        )
        for line in sale_order.order_line:
            line.product_id_change()

        sale_order.onchange_partner_id()
        sale_order._compute_tax_id()
        sale_order.action_confirm()

        self.partner2.with_context(**{"only_show_customer_id": True}).name_get()
        self.partner1.with_context(**{"only_show_customer_id": True}).name_get()
        wiz_act = partner_pool.open_wizard_action()
        partner_name = self.partner1.name
        partner_phone = self.partner1.phone
        merge_wizard = (
            self.env[wiz_act["res_model"]]
            .with_context(**wiz_act["context"])
            .create(
                {
                    "keep2": False,
                    "keep1": True,
                    "company_id2": self.env.user.company_id.id,
                    "company_name2": "Test Abc",
                    "phone2": "987654",
                    "mobile2": "+156778978",
                    "street2": "test street",
                    "street22": "test street 22",
                    "zip2": "202222",
                    "city2": "test city",
                    "state_id2": 1,
                    "country_id2": 2,
                    "is_company2": True,
                }
            )
        )
        merge_wizard._onchange_keep1()
        merge_wizard.with_context(
            **{
                "field_name": "name2",
            }
        ).swap_to_left()
        # change made from here
        merge_wizard.with_context(
            **{
                "field_name": "company_id2",
            }
        ).swap_to_left()
        merge_wizard.with_context(
            **{
                "field_name": "company_name2",
            }
        ).swap_to_left()
        merge_wizard.with_context(
            **{
                "field_name": "phone2",
            }
        ).swap_to_left()
        merge_wizard.with_context(
            **{
                "field_name": "mobile2",
            }
        ).swap_to_left()
        merge_wizard.with_context(
            **{
                "field_name": "street2",
            }
        ).swap_to_left()
        merge_wizard.with_context(
            **{
                "field_name": "street22",
            }
        ).swap_to_left()
        merge_wizard.with_context(
            **{
                "field_name": "zip2",
            }
        ).swap_to_left()
        merge_wizard.with_context(
            **{
                "field_name": "city2",
            }
        ).swap_to_left()
        merge_wizard.with_context(
            **{
                "field_name": "state_id2",
            }
        ).swap_to_left()
        merge_wizard.with_context(
            **{
                "field_name": "country_id2",
            }
        ).swap_to_left()
        merge_wizard.with_context(
            **{
                "field_name": "is_company2",
            }
        ).swap_to_left()
        merge_wizard.sudo().action_merge()
        partner_id = self.env["res.partner"].browse(self.partner2.id).exists()
        self.assertTrue(partner_id)
        self.assertEqual(partner_phone, merge_wizard.dst_partner_id.phone)
        self.assertEqual(partner_name, merge_wizard.dst_partner_id.name)
        self.assertEqual(self.partner2.id, merge_wizard.dst_partner_id.id)

    def test_merge_swap(self):
        partner_pool = self.env["res.partner"]
        self.partner1 = partner_pool.create(
            {
                "name": "test1",
                "email": "test@example.com",
                "phone": 987654,
            }
        )
        partner_pool |= self.partner1
        self.partner2 = partner_pool.create(
            {
                "name": "test1 (copy)",
                "email": "test@example.com",
                "phone": 987654321,
            }
        )
        partner_pool |= self.partner2
        proudct_id = self.env["product.product"].create(
            {
                "name": "test product A",
                "standard_price": 160,
                "list_price": 180,
                "type": "consu",
                "invoice_policy": "order",
                "expense_policy": "cost",
                "default_code": "PROD_COST",
                "service_type": "manual",
            }
        )
        sale_order = (
            self.env["sale.order"]
            .with_context(mail_notrack=True, mail_create_nolog=True)
            .create(
                {
                    "partner_id": self.partner1.id,
                    "partner_invoice_id": self.partner1.id,
                    "partner_shipping_id": self.partner1.id,
                    "order_line": [
                        (
                            0,
                            0,
                            {
                                "name": "test product A",
                                "product_id": proudct_id.id,
                                "product_uom_qty": 2,
                                "qty_delivered": 1,
                            },
                        )
                    ],
                }
            )
        )
        for line in sale_order.order_line:
            line.product_id_change()

        sale_order.onchange_partner_id()
        sale_order._compute_tax_id()
        sale_order.action_confirm()

        self.partner2.with_context(**{"only_show_customer_id": True}).name_get()
        self.partner1.with_context(**{"only_show_customer_id": True}).name_get()
        wiz_act = partner_pool.open_wizard_action()
        partner_name = self.partner1.name
        partner_phone = self.partner2.phone
        merge_wizard = (
            self.env[wiz_act["res_model"]]
            .with_context(**wiz_act["context"])
            .create({"keep2": True, "keep1": False})
        )
        merge_wizard._onchange_keep2()
        merge_wizard.with_context(
            **{
                "field_name": "name",
            }
        ).swap_to_right()
        merge_wizard.with_context(
            **{
                "field_name": "phone2",
            }
        ).swap_to_left()
        merge_wizard.action_merge()
        partner_id = self.env["res.partner"].browse(self.partner2.id).exists()
        self.assertTrue(partner_id)
        self.assertEqual(partner_phone, merge_wizard.dst_partner_id.phone)
        self.assertEqual(partner_name, merge_wizard.dst_partner_id.name)
        self.assertEqual(self.partner2.id, merge_wizard.dst_partner_id.id)

    def test_merge_skip(self):
        partner_pool = self.env["res.partner"]
        self.partner1 = partner_pool.create(
            {
                "name": "test1",
                "email": "test@example.com",
                "phone": 987654,
            }
        )
        partner_pool |= self.partner1
        self.partner2 = partner_pool.create(
            {
                "name": "test1 (copy)",
                "email": "test@example.com",
                "phone": 987654321,
            }
        )
        partner_pool |= self.partner2
        proudct_id = self.env["product.product"].create(
            {
                "name": "test product A",
                "standard_price": 160,
                "list_price": 180,
                "type": "consu",
                "invoice_policy": "order",
                "expense_policy": "cost",
                "default_code": "PROD_COST",
                "service_type": "manual",
            }
        )
        sale_order = (
            self.env["sale.order"]
            .with_context(mail_notrack=True, mail_create_nolog=True)
            .create(
                {
                    "partner_id": self.partner2.id,
                    "partner_invoice_id": self.partner2.id,
                    "partner_shipping_id": self.partner2.id,
                    "order_line": [
                        (
                            0,
                            0,
                            {
                                "name": "test product A",
                                "product_id": proudct_id.id,
                                "product_uom_qty": 2,
                                "qty_delivered": 1,
                            },
                        )
                    ],
                }
            )
        )
        for line in sale_order.order_line:
            line.product_id_change()

        sale_order.onchange_partner_id()
        sale_order._compute_tax_id()
        sale_order.action_confirm()
        self.partner2.with_context(**{"only_show_customer_id": True}).name_get()
        self.partner1.with_context(**{"only_show_customer_id": True}).name_get()
        wiz_act = partner_pool.open_wizard_action()
        merge_wizard = (
            self.env[wiz_act["res_model"]]
            .with_context(**wiz_act["context"])
            .create({"keep2": False, "keep1": True})
        )
        merge_wizard._onchange_keep1()
        merge_wizard.with_context(
            **{
                "field_name": "name",
            }
        ).swap_to_right()
        merge_wizard.with_context(
            **{
                "field_name": "phone2",
            }
        ).swap_to_left()
        merge_wizard.action_skip()
        partner_id1 = self.env["res.partner"].browse(self.partner1.id).exists()
        partner_id2 = self.env["res.partner"].browse(self.partner2.id).exists()
        self.assertTrue(partner_id1)
        self.assertTrue(partner_id2)
