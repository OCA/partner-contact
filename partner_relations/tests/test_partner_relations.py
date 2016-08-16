# -*- coding: utf-8 -*-
# Copyright 2015 Camptocamp SA
# Copyright 2016 Therp BV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields
from openerp.tests import common
from openerp.exceptions import ValidationError


class TestPartnerRelation(common.TransactionCase):

    def setUp(self):

        super(TestPartnerRelation, self).setUp()

        self.partner_model = self.env['res.partner']
        self.relation_type_model = self.env['res.partner.relation.type']
        self.relation_model = self.env['res.partner.relation']

        self.partner_1 = self.partner_model.create({
            'name': 'Test User 1',
            'is_company': False,
        })

        self.partner_2 = self.partner_model.create({
            'name': 'Test Company',
            'is_company': True,
        })

        self.relation_allow = self.relation_type_model.create({
            'name': 'allow',
            'name_inverse': 'allow_inverse',
            'contact_type_left': 'p',
            'contact_type_right': 'p',
            'allow_self': True
        })

        self.relation_disallow = self.relation_type_model.create({
            'name': 'disallow',
            'name_inverse': 'disallow_inverse',
            'contact_type_left': 'p',
            'contact_type_right': 'p',
            'allow_self': False
        })

        self.relation_default = self.relation_type_model.create({
            'name': 'default',
            'name_inverse': 'default_inverse',
            'contact_type_left': 'p',
            'contact_type_right': 'p',
        })

        self.relation_mixed = self.relation_type_model.create({
            'name': 'mixed',
            'name_inverse': 'mixed_inverse',
            'contact_type_left': 'c',
            'contact_type_right': 'p',
        })

        self.relation_symmetric = self.relation_type_model.create({
            'name': 'sym',
            'name_inverse': 'sym',
            'symmetric': True,
        })

    def test_self_allowed(self):
        self.relation_model.create({
            'type_id': self.relation_allow.id,
            'left_partner_id': self.partner_1.id,
            'right_partner_id': self.partner_1.id,
        })

    def test_self_disallowed(self):
        with self.assertRaises(ValidationError):
            self.relation_model.create({
                'type_id': self.relation_disallow.id,
                'left_partner_id': self.partner_1.id,
                'right_partner_id': self.partner_1.id,
            })

    def test_self_default(self):
        with self.assertRaises(ValidationError):
            self.relation_model.create({
                'type_id': self.relation_default.id,
                'left_partner_id': self.partner_1.id,
                'right_partner_id': self.partner_1.id,
            })

    def test_self_mixed(self):
        with self.assertRaises(ValidationError):
            self.relation_model.create({
                'type_id': self.relation_mixed.id,
                'left_partner_id': self.partner_1.id,
                'right_partner_id': self.partner_2.id,
            })

    def test_searching(self):
        relation = self.relation_model.create({
            'type_id': self.relation_mixed.id,
            'left_partner_id': self.partner_2.id,
            'right_partner_id': self.partner_1.id,
        })
        partners = self.env['res.partner'].search([
            ('search_relation_id', '=', relation.type_selection_id.id)
        ])
        self.assertTrue(self.partner_2 in partners)

        partners = self.env['res.partner'].search([
            ('search_relation_id', '!=', relation.type_selection_id.id)
        ])
        self.assertTrue(self.partner_1 in partners)

        partners = self.env['res.partner'].search([
            ('search_relation_id', '=', self.relation_mixed.name)
        ])
        self.assertTrue(self.partner_1 in partners)
        self.assertTrue(self.partner_2 in partners)

        partners = self.env['res.partner'].search([
            ('search_relation_id', '=', 'unknown relation')
        ])
        self.assertFalse(partners)

        partners = self.env['res.partner'].search([
            ('search_relation_partner_id', '=', self.partner_2.id),
        ])
        self.assertTrue(self.partner_1 in partners)

        partners = self.env['res.partner'].search([
            ('search_relation_date', '=', fields.Date.today()),
        ])
        self.assertTrue(self.partner_1 in partners)
        self.assertTrue(self.partner_2 in partners)

    def test_ui_functions(self):
        relation = self.relation_model.create({
            'type_id': self.relation_mixed.id,
            'left_partner_id': self.partner_2.id,
            'right_partner_id': self.partner_1.id,
        })
        self.assertEqual(relation.type_selection_id.type_id, relation.type_id)
        relation = relation.with_context(
            active_id=self.partner_1.id,
            active_ids=self.partner_1.ids,
            active_model='res.partner.relation',
        )
        relation.read()
        domain = relation._onchange_type_selection_id()['domain']
        self.assertTrue(
            ('is_company', '=', True) in domain['partner_id_display']
        )
        relation.write({
            'type_selection_id': relation.type_selection_id.id,
        })
        action = relation.get_action_related_partners()
        self.assertTrue(self.partner_1.id in action['domain'][0][2])

    def test_relation_all(self):
        relation_all_record = self.env['res.partner.relation.all']\
            .with_context(
                active_id=self.partner_2.id,
                active_ids=self.partner_2.ids,
        ).create({
            'other_partner_id': self.partner_1.id,
            'type_selection_id': self.relation_mixed.id * 10,
        })
        self.assertEqual(
            relation_all_record.display_name, '%s %s %s' % (
                self.partner_2.name,
                'mixed',
                self.partner_1.name,
            )
        )

        domain = relation_all_record.onchange_type_selection_id()['domain']
        self.assertTrue(
            ('is_company', '=', False) in domain['other_partner_id'])
        domain = relation_all_record.onchange_this_partner_id()['domain']
        self.assertTrue(
            ('contact_type_this', '=', 'c') in domain['type_selection_id'])

        relation_all_record.write({
            'type_id': self.relation_mixed.id,
        })
        relation = relation_all_record.relation_id
        relation_all_record.unlink()
        self.assertFalse(relation.exists())

    def test_symmetric(self):
        relation = self.relation_model.create({
            'type_id': self.relation_symmetric.id,
            'left_partner_id': self.partner_2.id,
            'right_partner_id': self.partner_1.id,
        })
        partners = self.env['res.partner'].search([
            ('search_relation_id', '=', relation.type_selection_id.id)
        ])
        self.assertTrue(self.partner_1 in partners)
        self.assertTrue(self.partner_2 in partners)
