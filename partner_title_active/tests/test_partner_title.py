# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.base.tests.common import BaseCommon


class TestPartnerTitle(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "A Partner",
                "title": cls.env.ref("base.res_partner_title_mister").id,
            }
        )

    def test_01_partner_title(self):
        self.assertTrue(self.partner.title.active, "Title should be active by default")
        self.partner.title.action_archive()
        self.assertFalse(
            self.partner.title.active, "Title should be inactive after archiving"
        )
