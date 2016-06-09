# -*- coding: utf-8 -*-
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests import common
from openerp.tools.safe_eval import safe_eval


class TestDeduplicateByWebsite(common.TransactionCase):
    def setUp(self):
        super(TestDeduplicateByWebsite, self).setUp()
        self.partner_1 = self.env['res.partner'].create({
            'name': 'Partner 1',
            'website': 'www.test-deduplicate.com',
        })
        self.partner_2 = self.env['res.partner'].create({
            'name': 'Partner 2',
            'website': 'www.test-deduplicate.com',
        })

    def test_deduplicate_by_website(self):
        wizard = self.env['base.partner.merge.automatic.wizard'].create({
            'group_by_website': True,
        })
        wizard.start_process_cb()
        found_match = False
        for line in wizard.line_ids:
            match_ids = safe_eval(line.aggr_ids)
            if (self.partner_1.id in match_ids and
                    self.partner_2.id in match_ids):
                found_match = True
                break
        self.assertTrue(found_match)
