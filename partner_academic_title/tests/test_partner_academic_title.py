# Copyright 2019 Luis M. Ontalba <luismaront@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo.tests import common


class TestPartnerAcademicTitle(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestPartnerAcademicTitle, cls).setUpClass()
        cls.partner_ac_tit_A = cls.env['partner.academic.title'].create({
            'name': 'A',
            'sequence': 2,
        })
        cls.partner_ac_tit_B = cls.env['partner.academic.title'].create({
            'name': 'B',
            'sequence': 1,
        })
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test partner',
        })

    def test_compute_academic_title_display(self):
        partner = self.partner
        partner.academic_title_ids = [
            (4, self.partner_ac_tit_A.id, 0),
            (4, self.partner_ac_tit_B.id, 0),
        ]
        self.assertEqual(partner.academic_title_display, "B, A")
