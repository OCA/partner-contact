# -*- coding: utf-8 -*-
# Copyright 2017 Therp BV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.exceptions import ValidationError
from odoo.tests import common


class TestPartnerHierarchy(common.TransactionCase):

    def test_hierarchy(self):
        """Test hierarchy.

        Create a hierarchical relation type. Then create a hierarchy
        of three levels.
        Check the computation of the display name.
        Check that no circular hierarchy can be created.
        """
        partner_model = self.env['res.partner']
        type_model = self.env['res.partner.relation.type']
        relation_model = self.env['res.partner.relation']
        partner_multinational = partner_model.create({
            'name': 'Big Important Multinational',
            'is_company': True,
            'ref': 'COM001'})
        partner_national = partner_model.create({
            'name': 'National Company',
            'is_company': True,
            'ref': 'COM002'})
        partner_local = partner_model.create({
            'name': 'Small local company',
            'is_company': True,
            'ref': 'COM003'})
        # Create a hierarchical relation type between companies:
        type_company2branch = type_model.create({
            'name': 'has daughter company',
            'name_inverse': 'has parent company',
            'contact_type_left': 'c',
            'contact_type_right': 'c',
            'hierarchy': 'left'})
        # Let the local company belong to the national company:
        relation_model.create({
            'left_partner_id': partner_national.id,
            'type_id': type_company2branch.id,
            'right_partner_id': partner_local.id})
        self.assertTrue(partner_local.has_partner_above)
        # We should be able to find the national company as being above
        # the local company.
        self.assertEqual(len(partner_local.partner_above_ids[0]), 1)
        self.assertEqual(
            partner_local.partner_above_ids[0].partner_above_id,
            partner_national)
        # Let the national company belong to the multinational company:
        relation_model.create({
            'left_partner_id': partner_multinational.id,
            'type_id': type_company2branch.id,
            'right_partner_id': partner_national.id})
        self.env.invalidate_all()
        self.assertFalse(partner_multinational.has_partner_above)
        self.assertTrue(partner_multinational.is_above(partner_local))
        self.assertEqual(
            partner_local.partner_above_hierarchy,
            '/'.join([partner_multinational.name, partner_national.name]))
        # Check error when trying to create inconsistent hierarchy:
        with self.assertRaises(ValidationError):
            relation_model.create({
                'left_partner_id': partner_local.id,
                'type_id': type_company2branch.id,
                'right_partner_id': partner_multinational.id})
