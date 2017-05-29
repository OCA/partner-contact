# -*- coding: utf-8 -*-
# © 2015 Antiun Ingenieria S.L. - Javier Iniesta
# © 2016 Tecnativa S.L. - Vicent Cubells
# © 2016 Tecnativa S.L. - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.exceptions import ValidationError


class TestResPartnerSector(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestResPartnerSector, cls).setUpClass()
        cls.Sector = cls.env['res.partner.sector']
        cls.sector_main = cls.Sector.create({
            'name': 'Test',
        })
        cls.sector_child = cls.Sector.create({
            'name': 'Test child',
            'parent_id': cls.sector_main.id,
        })

    def test_check_sectors(self):
        with self.assertRaises(ValidationError):
            self.env['res.partner'].create({
                'name': 'Test',
                'sector_id': self.sector_main.id,
                'secondary_sector_ids': [(4, self.sector_main.id)],
            })

    def test_check_recursion(self):
        with self.assertRaises(ValidationError):
            self.sector_main.parent_id = self.sector_child.id

    def test_name(self):
        self.assertEqual(
            self.sector_child.name_get()[0][1],
            "Test / Test child",
        )
