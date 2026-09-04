# Copyright 2019 Luis M. Ontalba <luismaront@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import Command
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPartnerAcademicTitle(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_ac_tit_a = cls.env["partner.academic.title"].create(
            {
                "name": "A",
                "sequence": 2,
            }
        )
        cls.partner_ac_tit_b = cls.env["partner.academic.title"].create(
            {
                "name": "B",
                "sequence": 1,
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test partner",
            }
        )

    def test_compute_academic_title_display(self):
        self.partner.academic_title_ids = [
            Command.link(self.partner_ac_tit_a.id),
            Command.link(self.partner_ac_tit_b.id),
        ]
        self.assertEqual(self.partner.academic_title_display, "B, A")
