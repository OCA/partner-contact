# -*- coding: utf-8 -*-
# Copyright 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests.common import TransactionCase


class TestPartnerLabel(TransactionCase):
    def test_partner_label(self):
        settings = self.env['base.config.settings'].create({})
        self.assertItemsEqual(
            settings.action_partner_labels_preview()['context']['active_ids'],
            self.env['res.partner'].search([], limit=100).ids,
        )
        self.assertEqual(
            settings.partner_labels_paperformat_id,
            self.env.ref('partner_label.report_res_partner_label')
            .paperformat_id
        )
        settings.partner_labels_paperformat_id = self.env.ref(
            'report.paperformat_us'
        ).id,
        self.assertEqual(
            self.env.ref('partner_label.report_res_partner_label')
            .paperformat_id,
            self.env.ref('report.paperformat_us')
        )
