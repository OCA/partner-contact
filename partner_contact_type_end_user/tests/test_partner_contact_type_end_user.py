# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestResPartnerType(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["res.partner"]

    def test_partner_type_end_user(self):
        """Test that a partner can be created with type 'end_user'"""
        partner = self.partner_model.create(
            {
                "name": "Test Partner",
                "type": "end_user",
            }
        )
        self.assertEqual(partner.type, "end_user", "Partner type should be 'end_user'")
