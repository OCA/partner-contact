# Copyright 2017 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestResPartnerRole(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.role1 = cls.env["res.partner.role"].create({"name": "Role 1"})
        cls.role2 = cls.env["res.partner.role"].create({"name": "Role 2"})

    def test_assign_roles_to_partner(self):
        """Test assigning roles to a partner"""
        self.partner.role_ids = [Command.set([self.role1.id, self.role2.id])]
        self.assertEqual(len(self.partner.role_ids), 2)
        self.assertIn(self.role1, self.partner.role_ids)
        self.assertIn(self.role2, self.partner.role_ids)

    def test_remove_roles_from_partner(self):
        """Test removing roles from a partner"""
        self.partner.role_ids = [Command.set([self.role1.id, self.role2.id])]
        self.partner.role_ids = [Command.set([])]
        self.assertEqual(len(self.partner.role_ids), 0)
