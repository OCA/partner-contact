# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

from odoo.tests.common import TransactionCase


class TestVatSanitized(TransactionCase):

    def test_vat_sanitized(self):
        ldlc = self.env['res.partner'].create({
            'name': 'LDLC',
            'is_company': True,
            'vat': 'fr 26 403 554 181'
            })
        self.assertEqual(ldlc.sanitized_vat, 'FR26403554181')
        # Also test invalidation
        ldlc.vat = False
        self.assertEqual(ldlc.sanitized_vat, False)
