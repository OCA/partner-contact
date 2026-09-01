# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import TransactionCase


class PartnerNamesOrder(TransactionCase):
    def order_set(self, order):
        config = self.env["res.config.settings"].create({"partner_names_order": order})
        config.execute()

    def test_get_computed_name(self):
        lastname = "García Lorca"
        firstname = "Federico"
        cases = (
            ("last_first", "García Lorca Federico"),
            ("last_first_comma", "García Lorca, Federico"),
            ("first_last", "Federico García Lorca"),
        )

        for order, name in cases:
            self.order_set(order)
            result = self.env["res.partner"]._get_computed_name(lastname, firstname)
            self.assertEqual(result, name)

    def test_get_inverse_name(self):
        lastname = "Flanker"
        firstname = "Petër"
        cases = (
            ("last_first", "Flanker Petër"),
            ("last_first_comma", "Flanker, Petër"),
            ("first_last", "Petër Flanker"),
        )
        for order, name in cases:
            self.order_set(order)
            result = self.env["res.partner"]._get_inverse_name(name)
            self.assertEqual(result["lastname"], lastname)
            self.assertEqual(result["firstname"], firstname)

    def test_name_create_empty(self):
        # See addons/mail/tests/test_res_partner.py test_name_create_corner_cases
        for name in ("", " ", False, None):
            with self.subTest(name=name):
                res_id = self.env["res.partner"].name_create("")[0]
                record = self.env["res.partner"].browse(res_id)
                self.assertEqual(record.name, "")
