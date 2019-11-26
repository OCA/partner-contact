# Copyright 2016 Tecnativa - Pedro M. Baeza
# Copyright 2018 Tecnativa - Cristina Martin
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.tools.safe_eval import safe_eval


class TestDeduplicateByWebsite(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_1 = (
            cls.env["res.partner"]
            .with_context(tracking_disable=True)
            .create(
                {
                    "name": "Partner 1",
                    "website": "www.test-deduplicate.com",
                    "email": "test@deduplicate.com",
                }
            )
        )

    def test_deduplicate_by_website(self):
        self.partner_2 = (
            self.env["res.partner"]
            .with_context(tracking_disable=True)
            .create(
                {
                    "name": "Partner 2",
                    "website": "www.test-deduplicate.com",
                    "email": "test2@deduplicate.com",
                }
            )
        )
        wizard = self.env["base.partner.merge.automatic.wizard"].create(
            {"group_by_website": True}
        )
        wizard.action_start_manual_process()
        found_match = False
        for line in wizard.line_ids:
            match_ids = safe_eval(line.aggr_ids)
            if self.partner_1.id in match_ids and self.partner_2.id in match_ids:
                found_match = True
                break
        self.assertTrue(found_match)

    def test_deduplicate_by_website_and_is_company(self):
        self.partner_2 = (
            self.env["res.partner"]
            .with_context(tracking_disable=True)
            .create(
                {
                    "name": "Partner 2",
                    "website": "www.test-deduplicate.com",
                    "email": "test@deduplicate.com",
                }
            )
        )
        wizard = self.env["base.partner.merge.automatic.wizard"].create(
            {"group_by_website": True, "group_by_email": True}
        )
        wizard.action_start_manual_process()
        found_match = False
        for line in wizard.line_ids:
            match_ids = safe_eval(line.aggr_ids)
            if self.partner_1.id in match_ids and self.partner_2.id in match_ids:
                found_match = True
                break
        self.assertTrue(found_match)
