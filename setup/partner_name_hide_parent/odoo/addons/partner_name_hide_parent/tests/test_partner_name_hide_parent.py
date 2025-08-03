# Copyright 2020-2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestPartnerNameHideParent(TransactionCase):
    def test_display_name(self):
        test_parent = self.env["res.partner"].create(
            {"name": "parent", "is_company": True}
        )
        test_child = self.env["res.partner"].create(
            {
                "name": "child",
                "is_company": False,
                "parent_id": test_parent.id,
                "hide_parent": True,
            }
        )
        self.assertEqual(test_child.display_name, "child")

        # Confirm that a change on "hide_parent" works as expected as a
        # trigger to update display_name
        test_child.write({"hide_parent": False})
        self.assertEqual(test_child.display_name, "parent, child")

        test_child.write({"hide_parent": True})
        self.assertEqual(test_child.display_name, "child")
