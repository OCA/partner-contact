# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase


class TestPartnerSalespersonPropagate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = cls.env["res.users"].create(
            {
                "name": "Test User",
                "login": "test_user",
            }
        )

        cls.parent_partner = cls.env["res.partner"].create(
            {
                "name": "Parent Partner",
                "user_id": cls.user.id,
            }
        )

        cls.child_partner = cls.env["res.partner"].create(
            {
                "name": "Child Partner",
                "parent_id": cls.parent_partner.id,
            }
        )

    def test_user_id_propagation(self):
        self.assertEqual(self.child_partner.user_id, self.parent_partner.user_id)

        new_user = self.env["res.users"].create(
            {
                "name": "New Test User",
                "login": "new_test_user",
            }
        )
        self.parent_partner.user_id = new_user.id

        self.assertEqual(self.child_partner.user_id, self.parent_partner.user_id)
