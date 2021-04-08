# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2021 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class PartnerNamesOrder(TransactionCase):
    def test_compute_name(self):
        lastname = "García Lorca"
        firstname = "Federico"
        cases = (
            ("last_first", "García Lorca Federico"),
            ("last_first_comma", "García Lorca, Federico"),
            ("first_last", "Federico García Lorca"),
        )
        partner_model = self.env["res.partner"]
        partner = partner_model.create(
            {"is_company": False, "firstname": firstname, "lastname": lastname}
        )
        for order, name in cases:
            partner.with_context(override_names_order=order)._compute_name()
            self.assertEqual(partner.name, name)

    def test_get_inverse_name(self):
        lastname = "Flanker"
        firstname = "Petër"
        cases = (
            ("last_first", "Flanker Petër"),
            ("last_first_comma", "Flanker, Petër"),
            ("first_last", "Petër Flanker"),
        )
        partner_model = self.env["res.partner"]
        for order, name in cases:
            result = partner_model.with_context(
                override_names_order=order
            )._get_inverse_name(name)
            self.assertEqual(result["lastname"], lastname)
            self.assertEqual(result["firstname"], firstname)
