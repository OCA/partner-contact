# -*- coding: utf-8 -*-
# Copyright 2014-2017 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from lxml import etree

from odoo.exceptions import ValidationError
from odoo.tests import common


class FakeTab():

    def __init__(self, id, name):
        self.id = id
        self.name = name


class TestPartnerTabs(common.SingleTransactionCase):

    post_install = True

    def test_create_tab(self):
        tab_model = self.env['res.partner.tab']
        partner_model = self.env['res.partner']
        new_tab = tab_model.create({
            'code': 'executive',
            'name': 'Executive members',
            'contact_type': 'c'})
        self.assertTrue(bool(new_tab))
        # There should now be a field in res_partner for the new tab.
        fieldname = partner_model._get_tab_fieldname(new_tab)
        self.assertTrue(fieldname in partner_model._fields)
        # The form view for partner should now also contain the tab,
        # if the view contains tabs in the first place.
        view_partner_form = self.env.ref('base.view_partner_form')
        view = partner_model.with_context().fields_view_get(
            view_id=view_partner_form.id, view_type='form')
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
        view = partner_model.with_context().fields_view_get(view_type='tree')
        tree = etree.fromstring(view['arch'])
        field = tree.xpath('//field[@name="%s"]' % fieldname)
        self.assertFalse(
            field,
            'Tab field %s should not exist in %s.' %
            (fieldname, etree.tostring(tree)))

    def test_tab_modifications(self):
        category_model = self.env['res.partner.category']
        tab_model = self.env['res.partner.tab']
        type_model = self.env['res.partner.relation.type']
        category_government = category_model.create({'name': 'Government'})
        executive_tab = tab_model.create({
            'code': 'executive',
            'name': 'Executive members'})
        self.assertTrue(bool(executive_tab))
        type_has_chairperson = type_model.create({
            'name': 'has chairperson',
            'name_inverse': 'is chairperson for',
            'contact_type_right': 'p',
            'tab_left_id': executive_tab.id})
        self.assertTrue(bool(type_has_chairperson))
        # If we change tab now to be only valid on company partners
        # the tab_left_id field should be cleared from the type:
        executive_tab.write({
            'contact_type': 'c',
            'partner_category_id': category_government.id})
        self.assertFalse(type_has_chairperson.tab_left_id.id)
        # Trying to set the tab back on type should be impossible:
        with self.assertRaises(ValidationError):
            type_has_chairperson.write({'tab_left_id': executive_tab.id})
        # We should be able to change tab, if also changing contact type
        # and category:
        type_has_chairperson.write({
            'partner_category_left': category_government.id,
            'contact_type_left': 'c',
            'tab_left_id': executive_tab.id})
        self.assertEqual(
            type_has_chairperson.tab_left_id.id,
            executive_tab.id)
        # Unlinking the tab should reset the tab name on relations:
        executive_tab.unlink()
        self.assertEqual(
            type_has_chairperson.tab_left_id.id,
            False)

    def test_relation_type_modifications(self):
        category_model = self.env['res.partner.category']
        tab_model = self.env['res.partner.tab']
        type_model = self.env['res.partner.relation.type']
        category_government = category_model.create({'name': 'Government'})
        category_positions = category_model.create({'name': 'Positions'})
        executive_tab = tab_model.create({
            'code': 'executive',
            'name': 'Executive members',
            'contact_type': 'c',
            'partner_category_id': category_government.id})
        self.assertTrue(bool(executive_tab))
        positions_tab = tab_model.create({
            'code': 'positions',
            'name': 'Positions held',
            'contact_type': 'p',
            'partner_category_id': category_positions.id})
        self.assertTrue(bool(executive_tab))
        type_has_chairperson = type_model.create({
            'name': 'has chairperson',
            'name_inverse': 'is chairperson for',
            'partner_category_left': category_government.id,
            'contact_type_left': 'c',
            'tab_left_id': executive_tab.id,
            'partner_category_right': category_positions.id,
            'contact_type_right': 'p',
            'tab_right_id': positions_tab.id})
        self.assertTrue(bool(type_has_chairperson))
        # Trying to clear either category should raise ValidationError:
        with self.assertRaises(ValidationError):
            type_has_chairperson.write({'partner_category_left': False})
        with self.assertRaises(ValidationError):
            type_has_chairperson.write({'partner_category_right': False})
        # Trying to clear either contact type should raise ValidationError:
        with self.assertRaises(ValidationError):
            type_has_chairperson.write({'contact_type_left': False})
        with self.assertRaises(ValidationError):
            type_has_chairperson.write({'contact_type_right': False})

    def test_relations(self):
        """Test relations shown on tab."""
        tab_model = self.env['res.partner.tab']
        type_model = self.env['res.partner.relation.type']
        partner_model = self.env['res.partner']
        relation_model = self.env['res.partner.relation']
        relation_all_model = self.env['res.partner.relation.all']
        executive_tab = tab_model.create({
            'code': 'executive',
            'name': 'Executive members'})
        self.assertTrue(bool(executive_tab))
        type_has_chairperson = type_model.create({
            'name': 'has chairperson',
            'name_inverse': 'is chairperson for',
            'contact_type_right': 'p',
            'tab_left_id': executive_tab.id})
        self.assertTrue(bool(type_has_chairperson))
        big_company = partner_model.create({
            'name': 'Big company',
            'is_company': True,
            'ref': 'BIG'})
        self.assertTrue(bool(big_company))
        important_person = partner_model.create({
            'name': 'Bart Simpson',
            'is_company': False,
            'ref': 'BS'})
        self.assertTrue(bool(important_person))
        relation_company_chair = relation_model.create({
            'left_partner_id': big_company.id,
            'type_id': type_has_chairperson.id,
            'right_partner_id': important_person.id})
        self.assertTrue(bool(relation_company_chair))
        # Now we should be able to find the relation with the tab_id:
        relation_all_company_chair = relation_all_model.search([
            ('tab_id', '=', executive_tab.id)], limit=1)
        self.assertTrue(bool(relation_all_company_chair))
        self.assertEqual(
            relation_company_chair.left_partner_id.id,
            relation_all_company_chair.this_partner_id.id)
        # We should find the company on the partner through tab field:
        fieldname = partner_model._get_tab_fieldname(executive_tab)
        self.assertTrue(fieldname in partner_model._fields)
        executive_partners = big_company[fieldname]
        self.assertEqual(len(executive_partners), 1)
        self.assertEqual(
            executive_partners.other_partner_id.id,
            important_person.id)
        #  When adding a new relation on a tab, type must be for tab.
        onchange_result = executive_partners.with_context(
            default_tab_id=executive_tab.id
        ).onchange_partner_id()
        self.assertTrue(onchange_result)
        self.assertIn('domain', onchange_result)
        self.assertIn('type_selection_id', onchange_result['domain'])
        self.assertEqual(
            onchange_result['domain']['type_selection_id'][-1],
            ('tab_id', '=', executive_tab.id))

    def test_update_tabs(self):
        """Test the function that will create tabs during module loading."""
        tab_model = self.env['res.partner.tab']
        partner_model = self.env['res.partner']
        executive_tab = tab_model.create({
            'code': 'executive',
            'name': 'Executive members'})
        self.assertTrue(bool(executive_tab))
        tabfield_executive_name = partner_model._get_tab_fieldname(
            executive_tab)
        # Create some fake tab fields (should be removed).
        tab_123 = FakeTab(123, 'First tab')
        tab_456 = FakeTab(456, 'Second tab')
        # Add "tab fields"
        partner_model._add_tab_field(tab_123)
        tabfield_123_name = partner_model._get_tab_fieldname(tab_123)
        self.assertEqual(
            partner_model._fields[tabfield_123_name].string, tab_123.name)
        partner_model._add_tab_field(tab_456)
        tabfield_456_name = partner_model._get_tab_fieldname(tab_456)
        self.assertEqual(
            partner_model._fields[tabfield_456_name].string, tab_456.name)
        # Now call hook method
        partner_model._register_hook()
        self.assertFalse(tabfield_123_name in partner_model._fields)
        self.assertFalse(tabfield_456_name in partner_model._fields)
        self.assertTrue(tabfield_executive_name in partner_model._fields)
