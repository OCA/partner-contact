from freezegun import freeze_time

from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestSaleCustomerOrderFrequency(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {"name": "Test Product", "type": "service"}
        )

    def _create_order(self, date_order, desired_state="sale"):
        with freeze_time(date_order):
            sale = self.env["sale.order"].create(
                {
                    "partner_id": self.partner.id,
                    "date_order": date_order,
                    "order_line": [
                        Command.create(
                            {
                                "product_id": self.product.id,
                                "price_unit": 100.0,
                            }
                        ),
                    ],
                }
            )
            if desired_state == "sale":
                sale.action_confirm()
            if desired_state == "cancel":
                sale.action_cancel()

        assert sale.state == desired_state
        return sale

    def test_no_orders(self):
        self.assertEqual(self.partner.average_order_duration, 0.0)
        self.assertEqual(self.partner.days_since_last_order, 0)
        self.assertEqual(self.partner.days_until_next_order, 0)

    def test_one_order(self):
        with freeze_time("2023-01-10"):
            self._create_order("2023-01-01")
            self.assertEqual(self.partner.average_order_duration, 0.0)
            self.assertEqual(self.partner.days_since_last_order, 9)
            self.assertEqual(self.partner.days_until_next_order, 0)

    def test_multiple_orders(self):
        # Order 1: 2023-01-01
        # Order 2: 2023-01-05 (gap 4 days)
        # Order 3: 2023-01-11 (gap 6 days)
        # Total gap: 10 days, 2 intervals. Avg = 5 days.
        # Last order: 2023-01-11
        # Today: 2023-01-20
        # Days since last: 9 days
        # Next order theoretically: 2023-01-11 + 5 days = 2023-01-16
        # Days until next: 2023-01-16 - 2023-01-20 = -4

        self._create_order("2023-01-01")
        self._create_order("2023-01-05")
        self._create_order("2023-01-11")

        with freeze_time("2023-01-20"):
            self.partner.invalidate_recordset()

            self.assertEqual(self.partner.average_order_duration, 5.0)
            self.assertEqual(self.partner.days_since_last_order, 9)
            self.assertEqual(self.partner.days_until_next_order, -4)

    def test_ignore_draft_cancelled(self):
        with freeze_time("2023-01-20"):
            self._create_order("2023-01-01", desired_state="sale")
            self._create_order("2023-01-05", desired_state="draft")
            self._create_order("2023-01-10", desired_state="cancel")

            self.partner.invalidate_recordset()
            # Should look like single order
            self.assertEqual(self.partner.average_order_duration, 0.0)
            self.assertEqual(self.partner.days_since_last_order, 19)
