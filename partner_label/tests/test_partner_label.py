# Copyright 2017 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class TestPartnerLabel(TransactionCase):
    def test_partner_label(self):
        settings = self.env["res.config.settings"].create({})
        settings.refresh()
        self.assertItemsEqual(
            settings.action_partner_labels_preview()["context"]["report_action"][
                "context"
            ]["active_ids"],
            self.env["res.partner"].search([], limit=100).ids,
        )
        self.assertEqual(
            settings.partner_labels_paperformat_id,
            self.env.ref("partner_label.report_res_partner_label").paperformat_id,
        )
        settings.partner_labels_paperformat_id = (
            self.env.ref("base.paperformat_us").id,
        )
        self.assertEqual(
            self.env.ref("partner_label.report_res_partner_label").paperformat_id,
            self.env.ref("base.paperformat_us"),
        )
