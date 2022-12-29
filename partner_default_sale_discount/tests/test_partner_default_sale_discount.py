# Copyright 2016 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from lxml import etree

from odoo.tests import common


class TestPartnerDefaultSaleDiscount(common.SavepointCase):
    def test_fields_view_get(self):
        res = self.env["sale.order"].fields_view_get(
            view_id=self.env.ref("sale.view_order_form").id, view_type="form"
        )
        eview = etree.fromstring(res["arch"])
        xml_order_line = eview.xpath("//field[@name='order_line']")
        self.assertTrue(xml_order_line)
        self.assertIn(
            "'default_discount': default_sale_discount",
            xml_order_line[0].get("context", "{}"),
        )
