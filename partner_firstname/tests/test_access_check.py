# -*- coding: utf-8 -*-
# Copyright 2016 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase
from openerp.exceptions import AccessError


class TestAccessCheck(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestAccessCheck, self).setUp(*args, **kwargs)

        self.user_a = self.env['res.users'].create({
            'name': u'User A',
            'login': u'user_a',
        })
        self.user_b = self.env['res.users'].create({
            'name': u'User B',
            'login': u'user_b',
        })

    def test_same_name_write(self):
        """Write only same name is allowed. Bug use case"""
        partner = self.user_b.partner_id.sudo(user=self.user_a.id)
        partner.write({'name': u'User B'})

    def test_other_name_write(self):
        """Write other name is not allowed. Normal case"""
        with self.assertRaises(AccessError):
            partner = self.user_b.partner_id.sudo(user=self.user_a.id)
            partner.write({'name': u'User C'})

    def test_other_fields_write(self):
        """Write other fields is not allowed. Normal case"""
        with self.assertRaises(AccessError):
            partner = self.user_b.partner_id.sudo(user=self.user_a.id)
            partner.write({'email': u't@e.com'})
