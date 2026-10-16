# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestGetView(TransactionCase):
    def test_get_view_arch_is_str(self):
        """get_view()['arch'] must stay a str, not bytes (regression test).

        res.partner's own parent_id (many2one to res.partner) is enough to
        trigger the override on its own form view, with no other module
        or fake model needed.
        """
        result = self.env["res.partner"].get_view(view_type="form")
        self.assertIsInstance(result["arch"], str)
