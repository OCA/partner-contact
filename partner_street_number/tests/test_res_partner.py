# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestResPartner(TransactionCase):

    def setUp(self):
        super(TestResPartner, self).setUp()
        self.main_partner = self.env.ref('base.main_partner')

    def test_display_address(self):
        # method name_get() having show_address=True in context
        # will invoke method _display_address()
        partner_test = self.main_partner.with_context(show_address=True)
        displayed_name = partner_test.name_get()

        self.assertEqual(
            displayed_name[0][1],
            'YourCompany\n1725 Slough Ave.\nScranton PA 18540\nUnited States'
        )
