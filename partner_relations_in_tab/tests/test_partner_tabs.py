# -*- coding: utf-8 -*-
# Copyright 2014-2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from lxml import etree

from openerp.tests import common


class TestPartnerTabs(common.SingleTransactionCase):

    post_install = True

    def _get_tab_fieldname(self, relation_type, side):
        tab = self._get_tab(relation_type, side)
        return tab.get_fieldname()

    def _get_tab(self, relation_type, side):
        partner_model = self.registry('res.partner')
        return partner_model._make_tab(relation_type, side)

    def test_create_tab(self):
        cr, uid = self.cr, self.uid
        type_model = self.registry('res.partner.relation.type')
        partner_model = self.registry('res.partner')
        type_has_chairperson_id = type_model.create(
            cr, uid, {
                'name': 'has chairperson',
                'name_inverse': 'is chairperson for',
                'contact_type_left': 'c',
                'own_tab_left': True,
                'contact_type_right': 'p'})
        type_has_chairperson = type_model.browse(
            cr, uid, type_has_chairperson_id)
        self.assertTrue(bool(type_has_chairperson))
        # There should now be a field in res_partner for the new tab:
        fieldname = self._get_tab_fieldname(type_has_chairperson, 'left')
        self.assertTrue(fieldname in partner_model._columns)
        # The form view for partner should now also contain the tab:
        view = partner_model.fields_view_get(cr, uid, view_type='form')
        tree = etree.fromstring(view['arch'])
        field = tree.xpath('//field[@name="id"]')
        self.assertTrue(field, 'Id field does not exist.')
        # And we should have a field for the tab:
        field = tree.xpath('//field[@name="%s"]' % fieldname)
        self.assertTrue(
            field,
            'Tab field %s does not exist in %s.' %
            (fieldname, etree.tostring(tree)))
        # There should be no effect on the tree view:
        view = partner_model.fields_view_get(cr, uid, view_type='tree')
        tree = etree.fromstring(view['arch'])
        field = tree.xpath('//field[@name="%s"]' % fieldname)
        self.assertFalse(
            field,
            'Tab field %s should not exist in %s.' %
            (fieldname, etree.tostring(tree)))

    def test_relations(self):
        """Test relations shown on tab."""
        cr, uid = self.cr, self.uid
        type_model = self.registry('res.partner.relation.type')
        relation_model = self.registry('res.partner.relation')
        partner_model = self.registry('res.partner')
        type_has_chairperson_id = type_model.create(
            cr, uid, {
                'name': 'has chairperson',
                'name_inverse': 'is chairperson for',
                'contact_type_left': 'c',
                'own_tab_left': True,
                'contact_type_right': 'p'})
        type_has_chairperson = type_model.browse(
            cr, uid, type_has_chairperson_id)
        self.assertTrue(bool(type_has_chairperson))
        big_company_id = partner_model.create(
            cr, uid, {
                'name': 'Big company',
                'is_company': True,
                'ref': 'BIG'})
        big_company = partner_model.browse(cr, uid, big_company_id)
        self.assertTrue(bool(big_company))
        important_person_id = partner_model.create(
            cr, uid, {
                'name': 'Bart Simpson',
                'is_company': False,
                'ref': 'BS'})
        important_person = partner_model.browse(cr, uid, important_person_id)
        self.assertTrue(bool(important_person))
        relation_company_chair_id = relation_model.create(
            cr, uid, {
                'left_partner_id': big_company.id,
                'type_id': type_has_chairperson.id,
                'right_partner_id': important_person.id})
        relation_company_chair = relation_model.browse(
            cr, uid, relation_company_chair_id)
        self.assertTrue(bool(relation_company_chair))
        # There should now be a field in res_partner for the new tab:
        fieldname = self._get_tab_fieldname(type_has_chairperson, 'left')
        self.assertTrue(fieldname in partner_model._columns)
        # We should find the chairperson of the company through the tab:
        executive_partners = big_company[fieldname]
        self.assertEqual(len(executive_partners), 1)
        self.assertEqual(
            executive_partners[0].right_partner_id.id,
            important_person.id)

    def test_update_tabs(self):
        """Test the function that will create tabs during module loading."""
        cr, uid = self.cr, self.uid
        type_model = self.registry('res.partner.relation.type')
        partner_model = self.registry('res.partner')
        type_has_chairperson_id = type_model.create(
            cr, uid, {
                'name': 'has chairperson',
                'name_inverse': 'is chairperson for',
                'contact_type_left': 'c',
                'own_tab_left': True,
                'contact_type_right': 'p'})
        type_has_chairperson = type_model.browse(
            cr, uid, type_has_chairperson_id)
        # Now call hook method
        partner_model._register_hook(cr)
        # There should now be a field in res_partner for the new tab:
        fieldname = self._get_tab_fieldname(type_has_chairperson, 'left')
        self.assertTrue(fieldname in partner_model._columns)
