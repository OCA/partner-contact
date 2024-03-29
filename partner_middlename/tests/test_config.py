# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestConfig(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wizard = cls.env["res.config.settings"].create({})
        cls.partner = cls.env["res.partner"].create(
            {"firstname": "First", "middlename": "Middle", "lastname": "Last"}
        )

    def test_last_first(self):
        self.wizard.partner_names_order = "last_first"
        self.wizard.set_values()
        self.wizard.action_recalculate_partners_name()
        self.assertEqual(self.partner.name, "Last First Middle")

    def test_last_first_comma(self):
        self.wizard.partner_names_order = "last_first_comma"
        self.wizard.set_values()
        self.wizard.action_recalculate_partners_name()
        self.assertEqual(self.partner.name, "Last, First Middle")

    def test_first_last(self):
        self.wizard.partner_names_order = "first_last"
        self.wizard.set_values()
        self.wizard.action_recalculate_partners_name()
        self.assertEqual(self.partner.name, "First Middle Last")
