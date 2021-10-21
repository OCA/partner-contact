# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo.tests.common import SavepointCase


class TestPartnerTitle(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

    def test_default_order(self):
        partner_titles = self.env["res.partner.title"].search([])
        self.assertEqual(
            partner_titles.mapped("name"),
            partner_titles.sorted(lambda x: x.name).mapped("name"),
        )

    def test_sequence_order(self):
        partner_titles = self.env["res.partner.title"].search([])
        partner_first = partner_titles[0]
        partner_first.sequence = 100
        partner_last = partner_titles[-1]
        partner_last.sequence = 0
        partner_titles = self.env["res.partner.title"].search([])
        self.assertEqual(
            partner_titles.mapped("name"),
            partner_titles.sorted(lambda x: (x.sequence, x.name)).mapped("name"),
        )
        # last and first inverted
        self.assertEqual(partner_titles[0], partner_last)
        self.assertEqual(partner_titles[-1], partner_first)
