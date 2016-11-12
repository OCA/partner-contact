# -*- coding: utf-8 -*-
# © 2015 Antiun Ingenieria S.L. - Javier Iniesta
# © 2016 Tecnativa S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError


class TestResPartner(TransactionCase):

    def test_check_sectors(self):
        sector = self.env['res.partner.sector'].create({'name': 'Test'})
        with self.assertRaises(ValidationError):
            self.env['res.partner'].create(
                {'name': 'Test', 'sector_id': sector.id,
                 'secondary_sector_ids': [(4, sector.id)]})
