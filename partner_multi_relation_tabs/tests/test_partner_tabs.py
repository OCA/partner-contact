# Copyright 2014-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from lxml import etree

from odoo.exceptions import ValidationError

from . import common
from ..tablib import Tab


class TestPartnerTabs(common.TestCommon):
    post_install = True

    def test_create_tab(self):
        self.assertTrue(bool(self.tab_board))
        tab_obj = Tab(self.tab_board)
        # fields_view_get should force the creation of the new tabs.
        view_partner_form = self.env.ref('base.view_partner_form')
        view = self.partner_model.with_context().fields_view_get(
            view_id=view_partner_form.id, view_type='form')
        # The form view for partner should now also contain field 'id'.
        tree = etree.fromstring(view['arch'])
        field = tree.xpath('//field[@name="id"]')
        self.assertTrue(field, 'Id field does not exist.')
        # There should now be a field in res_partner for the new tab.
        fieldname = tab_obj.get_fieldname()
        self.assertTrue(fieldname in self.partner_model._fields)
        # And we should have a field for the tab:
        field = tree.xpath('//field[@name="%s"]' % fieldname)
        self.assertTrue(
            field,
            'Tab field %s does not exist in %s.' %
            (fieldname, etree.tostring(tree)))
        # There should be no effect on the tree view:
        view = self. partner_model.with_context().fields_view_get(
            view_type='tree')
        tree = etree.fromstring(view['arch'])
        field = tree.xpath('//field[@name="%s"]' % fieldname)
        self.assertFalse(
            field,
            'Tab field %s should not exist in %s.' %
            (fieldname, etree.tostring(tree)))

    def test_view_without_pages(self):
        """Check that _add_tab_pages does not effect view without pages."""
        # pylint: disable=protected-access
        view = etree.Element('view')
        extra_fields = self.partner_model._add_tab_pages(view)
        self.assertFalse(extra_fields)

    def test_tab_modifications(self):
        tab_executive = self.tab_model.create({
            'code': 'executive',
            'name': 'Executive members'})
        self.assertTrue(bool(tab_executive))
        type_chairperson = self.type_model.create({
            'name': 'has chairperson',
            'name_inverse': 'is chairperson for',
            'contact_type_left': 'p',  # This emulates a user mistake.
            'contact_type_right': 'p',
            'tab_left_id': tab_executive.id})
        self.assertTrue(bool(type_chairperson))
        # If we change tab now to be only valid on company partners
        # the tab_left_id field should be cleared from the type:
        tab_executive.write({'contact_type': 'c'})
        self.assertFalse(type_chairperson.tab_left_id.id)
        # Trying to set the tab back on type should be impossible:
        with self.assertRaises(ValidationError):
            type_chairperson.write({'tab_left_id': tab_executive.id})
        # We should be able to change tab, if also changing contact type.
        type_chairperson.write({
            'contact_type_left': 'c',
            'tab_left_id': tab_executive.id})
        self.assertEqual(
            type_chairperson.tab_left_id.id,
            tab_executive.id)
        # Unlinking the tab should reset the tab_left_id on relation type.
        tab_executive.unlink()
        self.assertEqual(
            type_chairperson.tab_left_id.id,
            False)
        # It should not be possible to add category or contact type to as
        # selection criteria to a tab meant for specific partners.
        with self.assertRaises(ValidationError):
            self.tab_departments.write({'contact_type': 'c'})
        with self.assertRaises(ValidationError):
            self.tab_departments.write({
                'partner_category_id': self.category_government.id})

    def test_type_modifications(self):
        self.assertTrue(bool(self.tab_board))
        self.assertTrue(bool(self.tab_positions))
        self.assertTrue(bool(self.type_chairperson))
        # Trying to clear either category should raise ValidationError:
        with self.assertRaises(ValidationError):
            self.type_chairperson.write({'partner_category_left': False})
        with self.assertRaises(ValidationError):
            self.type_chairperson.write({'partner_category_right': False})
        # Trying to clear either contact type should raise ValidationError:
        with self.assertRaises(ValidationError):
            self.type_chairperson.write({'contact_type_left': False})
        with self.assertRaises(ValidationError):
            self.type_chairperson.write({'contact_type_right': False})

    def test_relations(self):
        """Test relations shown on tab."""
        relation_all_model = self.env['res.partner.relation.all']
        self.assertTrue(bool(self.tab_board))
        self.assertTrue(bool(self.type_ceo))
        self.assertTrue(bool(self.partner_big_company))
        self.assertTrue(bool(self.partner_important_person))
        self.assertTrue(bool(self.relation_company_ceo))
        # Now we should be able to find the relation with the tab_id:
        board_partners = relation_all_model.search([
            ('tab_id', '=', self.tab_board.id)])
        self.assertTrue(bool(board_partners))
        self.assertIn(
            self.partner_big_company,
            [relation.this_partner_id for relation in board_partners])
        # We should find the company on the partner through tab field:
        tab_obj = Tab(self.tab_board)
        fieldname = tab_obj.get_fieldname()
        self.assertTrue(fieldname in self.partner_model._fields)
        board_partners = self.partner_big_company[fieldname]
        self.assertEqual(len(board_partners), 1)
        self.assertEqual(
            board_partners.other_partner_id.id,
            self.partner_important_person.id)
        #  When adding a new relation on a tab, type must be for tab.
        onchange_result = board_partners.with_context(
            default_tab_id=self.tab_board.id
        ).onchange_partner_id()
        self.assertTrue(onchange_result)
        self.assertIn('domain', onchange_result)
        self.assertIn('type_selection_id', onchange_result['domain'])
        self.assertEqual(
            onchange_result['domain']['type_selection_id'][-1],
            ('tab_id', '=', self.tab_board.id))

    def test_compute_visibility(self):
        """Check the computation of visibility on partners."""
        # pylint: disable=protected-access
        main_partner = self.env.ref('base.main_partner')
        main_partner._compute_tabs_visibility()
        tab_obj = Tab(self.tab_departments)
        fieldname = tab_obj.get_fieldname()
        visible_fieldname = tab_obj.get_visible_fieldname()
        self.assertIn(visible_fieldname, main_partner._fields)
        self.assertIn(fieldname, main_partner._fields)
        self.assertEqual(main_partner[visible_fieldname], True)
        department_relations = main_partner[fieldname]
        self.assertTrue(len(department_relations) >= 1)
        departments = [
            relation.other_partner_id for relation in department_relations]
        for department in departments:
            self.assertIn(
                self.category_department, department.category_id)
