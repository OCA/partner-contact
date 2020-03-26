# Copyright 2017 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2020 Manuel Calero - Tecnativa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.tools.safe_eval import safe_eval


class TestDeduplicateByRef(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner_1 = self.env["res.partner"].create(
            {"name": "Partner 1", "ref": "123456", "email": "test@deduplicate.com"}
        )
        self.partner_2 = self.env["res.partner"].create(
            {"name": "Partner 2", "ref": "123456", "email": "test@deduplicate.com"}
        )

    def test_deduplicate_by_ref(self):
        wizard = self.env["base.partner.merge.automatic.wizard"].create(
            {"group_by_ref": True}
        )
        wizard.action_start_manual_process()
        found_match = False
        for line in wizard.line_ids:
            match_ids = safe_eval(line.aggr_ids)
            if self.partner_1.id in match_ids and self.partner_2.id in match_ids:
                found_match = True
                break
        self.assertTrue(found_match)

    def test_deduplicate_by_ref_and_is_company(self):
        wizard = self.env["base.partner.merge.automatic.wizard"].create(
            {"group_by_ref": True, "group_by_email": True}
        )
        wizard.action_start_manual_process()
        found_match = False
        for line in wizard.line_ids:
            match_ids = safe_eval(line.aggr_ids)
            if self.partner_1.id in match_ids and self.partner_2.id in match_ids:
                found_match = True
                break
        self.assertTrue(found_match)
