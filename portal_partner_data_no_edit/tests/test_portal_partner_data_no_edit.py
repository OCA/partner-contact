# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import tagged, common


@tagged('post_install', '-at_install')
class PortalHttpCase(common.HttpCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env.ref("base.partner_demo_portal")

    def test_portal_partner_default(self):
        """The default standard behavior"""
        tour = (
            "odoo.__DEBUG__.services['web_tour.tour']",
            "portal_partner_data_no_edit_default_tour",
        )
        self.browser_js(
            url_path="/my",
            code="%s.run('%s')" % tour,
            ready="%s.tours.%s.ready" % tour,
            login="portal",
        )

    def test_portal_partner_blocked(self):
        """There's no form fields anymore"""
        self.partner.block_portal_data_edit = True
        tour = (
            "odoo.__DEBUG__.services['web_tour.tour']",
            "portal_partner_data_no_edit_block_tour",
        )
        self.browser_js(
            url_path="/my",
            code="%s.run('%s')" % tour,
            ready="%s.tours.%s.ready" % tour,
            login="portal",
        )
