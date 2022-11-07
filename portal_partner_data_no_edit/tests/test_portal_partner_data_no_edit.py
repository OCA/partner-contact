# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import common, tagged


@tagged("-at_install", "post_install")
class PortalHttpCase(common.HttpCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env.ref("base.partner_demo_portal")

    def test_portal_partner_default(self):
        """The default standard behavior"""
        self.start_tour(
            "/my", "portal_partner_data_no_edit_default_tour", login="portal"
        )

    def test_portal_partner_blocked(self):
        """There's no form fields anymore"""
        self.partner.block_portal_data_edit = True
        self.start_tour("/my", "portal_partner_data_no_edit_block_tour", login="portal")
