# -*- coding: utf-8 -*-
# © 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class PartnerNamesOrder(TransactionCase):
    def order_set(self, order):
        return self.env['ir.config_parameter'].set_param(
            'partner_names_order', order)

    def test_get_computed_name(self):
        lastname = u"García Lorca"
        firstname = u"Federico"
        cases = (
            ('last_first', u"García Lorca Federico"),
            ('last_first_comma', u"García Lorca, Federico"),
            ('first_last', u"Federico García Lorca"),
        )

        for order, name in cases:
            self.order_set(order)
            result = self.env['res.partner']._get_computed_name(
                lastname, firstname)
            self.assertEqual(result, name)

    def test_get_inverse_name(self):
        lastname = u"Flanker"
        firstname = u"Petër"
        cases = (
            ('last_first', u"Flanker Petër"),
            ('last_first_comma', u"Flanker, Petër"),
            ('first_last', u"Petër Flanker"),
        )
        for order, name in cases:
            self.order_set(order)
            result = self.env['res.partner']._get_inverse_name(name)
            self.assertEqual(result['lastname'], lastname)
            self.assertEqual(result['firstname'], firstname)
