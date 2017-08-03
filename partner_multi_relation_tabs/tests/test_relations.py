# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common
from lxml import etree


class TestRelations(common.SingleTransactionCase):

    post_install = True

    def test_person_to_person_relation(self):
        res_partner_relation_type_model = self.env['res.partner.relation.type']
        res_partner_relation_type_selection_model = self.env[
            'res.partner.relation.type.selection']
        p2p_rel = res_partner_relation_type_model.create({
            'name': 'Employer',
            'contact_type_left': 'p',
            'name_inverse': 'Employee',
            'contact_type_right': 'p'
        })
        p2p_rel.write({'own_tab_left': True})
        p2p_rel_typ = res_partner_relation_type_selection_model.search(
            [('type_id', '=', p2p_rel.id)], limit=1).id
        res_partner_model = self.env['res.partner']
        employer = res_partner_model.create({'name': 'Employer'})
        employee = res_partner_model.create({'name': 'Employee'})
        res_partner_relation_all_model = self.env['res.partner.relation.all']
        res_partner_relation_all_model.create({
            'this_partner_id': employer.id,
            'other_partner_id': employee.id,
            'type_selection_id': p2p_rel_typ
        })
        result = employer.with_context().fields_view_get()
        # we check whether the company's res.partner form contains the
        # appropriate views (inserted by fields_view_get
        tree = etree.fromstring(result['arch'])
        field = tree.xpath('field[@name="id"]')
        self.assertTrue(field, 'Id field does not exist.')
        # initially we should have the left and not the right
        self.assertTrue('relation_ids_own_tab_{}_left'.format(
            p2p_rel.id in employee._fields))
        self.assertTrue('relation_ids_own_tab_{}_right'.format(
            p2p_rel.id not in employee._fields))
        p2p_rel.write({'is_symmetric': True})
        # now we should have them both
        self.assertTrue('relation_ids_own_tab_{}_left'.format(
            p2p_rel.id in employee._fields))
        self.assertTrue('relation_ids_own_tab_{}_right'.format(
            p2p_rel.id in employee._fields))

    def test_person_to_company_relation(self):
        res_partner_relation_type_model = self.env['res.partner.relation.type']
        res_partner_relation_type_selection_model = self.env[
            'res.partner.relation.type.selection']
        res_partner_relation_all_model = self.env['res.partner.relation.all']
        res_partner_model = self.env['res.partner']
        company = res_partner_model.create({
            'name': 'Company',
            'is_company': True
        })
        employer = res_partner_model.create({'name': 'Employer'})
        c2p_rel = res_partner_relation_type_model.create({
            'name': 'Company',
            'contact_type_left': 'c',
            'name_inverse': 'Employee',
            'contact_type_right': 'p'
        })
        c2p_rel.write({'own_tab_left': True})
        c2p_rel.write({'own_tab_right': True})
        c2p_rel_typ = res_partner_relation_type_selection_model.search(
            [('type_id', '=', c2p_rel.id)], limit=1).id
        res_partner_relation_all_model.create({
            'this_partner_id': company.id,
            'other_partner_id': employer.id,
            'type_selection_id': c2p_rel_typ
        })
        result = employer.with_context().fields_view_get()
        # we check whether the company's res.partner form contains the
        # appropriate views (inserted by fields_view_get
        tree = etree.fromstring(result['arch'])
        field = tree.xpath('field[@name="id"]')
        self.assertTrue(field, 'Id field does not exist.')
        relation_ids_value_right = getattr(
            employer,
            'relation_ids_own_tab_{}_right'.format(c2p_rel.id))
        self.assertTrue(
            relation_ids_value_right,
            'Relation was not found')
        relation_ids_value_left = getattr(
            company, 'relation_ids_own_tab_{}_left'.format(c2p_rel.id))
        self.assertTrue(
            relation_ids_value_left,
            'Left relation field was not found')
