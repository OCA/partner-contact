# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestPartnerTitle(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Partner = cls.env["res.partner"]

    def test_01_partner_title(self):
        partner = self.Partner.create({"name": "A Partner"})
        self.assertTrue(partner.active, "Partner should be active by default")
        partner.action_archive()
        self.assertFalse(partner.active, "Partner should be inactive after archiving")
