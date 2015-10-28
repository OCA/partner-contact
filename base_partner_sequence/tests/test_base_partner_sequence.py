# -*- coding: utf-8 -*-
# © 2015 ACSONE SA/NV (<http://acsone.eu>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import openerp.tests.common as common


class TestBasePartnerSequence(common.TransactionCase):

    def test_ref_sequence_on_partner(self):
        res_partner = self.env['res.partner']
        partner = res_partner.create({
            'name': "test1",
            'email': "test@test.com"})
        self.assertTrue(partner.ref, "A partner has always a ref.")

        copy = partner.copy()
        self.assertTrue(copy.ref, "A partner with ref created by copy "
                        "has a ref by default.")
