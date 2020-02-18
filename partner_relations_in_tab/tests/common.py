# -*- coding: utf-8 -*-
# Copyright 2014-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests import common


class TestCommon(common.SingleTransactionCase):

    post_install = True

    def setUp(self):
        super(TestCommon, self).setUp()
        self.type_model = self.registry('res.partner.relation.type')
        self.category_model = self.registry('res.partner.category')
        self.partner_model = self.registry('res.partner')
        self.relation_model = self.registry('res.partner.relation')
        self.type_has_chairperson = self._make_relation_type({
            'name': 'has chairperson',
            'name_inverse': 'is chairperson for',
            'contact_type_left': 'c',
            'own_tab_left': True,
            'contact_type_right': 'p'})
        self.chairperson_tab = self.type_model.make_tab(
            self.type_has_chairperson, 'left')
        self.child_category = self._make_category({'name': 'child'})
        self.type_is_father = self._make_relation_type({
            'name': 'is father',
            'name_inverse': 'is child of',
            'contact_type_left': 'p',
            'own_tab_left': True,
            'contact_type_right': 'p',
            'partner_category_right': self.child_category.id})
        self.is_father_tab = self.type_model.make_tab(
            self.type_is_father, 'left')

    def _make_relation_type(self, vals):
        cr, uid = self.cr, self.uid
        relation_type_id = self.type_model.create(cr, uid, vals)
        relation_type = self.type_model.browse(
            cr, uid, relation_type_id)
        self.assertTrue(bool(relation_type))
        return relation_type

    def _make_partner(self, vals):
        cr, uid = self.cr, self.uid
        partner_id = self.partner_model.create(cr, uid, vals)
        partner = self.partner_model.browse(cr, uid, partner_id)
        self.assertTrue(bool(partner))
        return partner

    def _make_relation(self, vals):
        cr, uid = self.cr, self.uid
        relation_id = self.relation_model.create(cr, uid, vals)
        relation = self.relation_model.browse(cr, uid, relation_id)
        self.assertTrue(bool(relation))
        return relation

    def _make_category(self, vals):
        cr, uid = self.cr, self.uid
        category_id = self.category_model.create(cr, uid, vals)
        category = self.category_model.browse(cr, uid, category_id)
        self.assertTrue(bool(category))
        return category
