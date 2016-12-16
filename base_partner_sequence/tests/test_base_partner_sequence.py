# -*- coding: utf-8 -*-
# © 2015 ACSONE SA/NV (<http://acsone.eu>).
# © 2016 syscoon GmbH (<http://syscoon.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import openerp.tests.common as common


class TestBasePartnerSequence(common.TransactionCase):

    def test_ref_sequence_on_partner(self):
        res_partner = self.env['res.partner']
        partner_customer = res_partner.create({
            'name': "Customer Test",
            'email': "customer@test.com",
            'customer': True})
        self.assertTrue(partner_customer.ref, "A customer has always a ref.")

        copy = partner_customer.copy()
        self.assertTrue(copy.ref, "A customer with ref created by copy "
                        "has a ref by default.")

        partner_supplier = res_partner.create({
            'name': "Supplier Test",
            'email': "supplier@test.com"})
        self.assertTrue(partner_supplier.ref, "A supplier has always a ref.")

        copy = partner_supplier.copy()
        self.assertTrue(copy.ref, "A supplier with ref created by copy "
                        "has a ref by default.")
