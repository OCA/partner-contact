# -*- coding: utf-8 -*-
# Copyright 2016 Acsone S.A.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.exceptions import ValidationError
from openerp.tests.common import TransactionCase


class TestGLN(TransactionCase):
    def setUp(self):
        super(TestGLN, self).setUp()
        self.partner = self.env['res.partner'].create({'name': 'TestGLN'})
        self.partner2 = self.env['res.partner'].create({'name': 'TestGLN2'})

    def test_gln(self):
        # Good GLN
        self.partner.write({'gln': '5450534001717'})
        self.assertEqual(self.partner.gln, '5450534001717')

        # Duplicate GLN
        try:
            self.partner2.write({'gln': '5450534001717'})
        except ValidationError, e:
            self.assertEqual(
                e.value,
                "GLN code is already used by existing partners : TestGLN")

        # Bad GLN
        try:
            self.partner.gln = '5450534001716'
        except ValidationError, e:
            self.assertEqual(
                e.value,
                "The GLN field for the partner TestGLN is not valid! "
                "The number's checksum or check digit is invalid.")
