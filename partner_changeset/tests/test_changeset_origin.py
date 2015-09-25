# -*- coding: utf-8 -*-
#
#
#    Authors: Guewen Baconnier
#    Copyright 2015 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from openerp.tests import common
from .common import ChangesetMixin


class TestChangesetOrigin(ChangesetMixin, common.TransactionCase):
    """ Check that origin - old fields are stored as expected.

    'origin' fields dynamically read fields from the partner when the state
    of the change is 'draft'. Once a change becomes 'done' or 'cancel', the
    'old' field copies the value from the partner and then the 'origin' field
    displays the 'old' value.
    """

    def _setup_rules(self):
        ChangesetFieldRule = self.env['changeset.field.rule']
        ChangesetFieldRule.search([]).unlink()
        partner_model_id = self.env.ref('base.model_res_partner').id
        self.field_name = self.env.ref('base.field_res_partner_name')
        ChangesetFieldRule.create({
            'model_id': partner_model_id,
            'field_id': self.field_name.id,
            'action': 'validate',
        })

    def setUp(self):
        super(TestChangesetOrigin, self).setUp()
        self._setup_rules()
        self.partner = self.env['res.partner'].create({
            'name': 'X',
        })

    def test_origin_value_of_change_with_apply(self):
        """ Origin field is read from the parter or 'old' - with apply

        According to the state of the change.
        """
        self.partner.with_context(__changeset_rules=True).write({
            'name': 'Y',
        })
        changeset = self.partner.changeset_ids
        change = changeset.change_ids
        self.assertEqual(self.partner.name, 'X')
        self.assertEqual(change.origin_value_char, 'X')
        self.assertEqual(change.origin_value_display, 'X')
        self.partner.write({'name': 'A'})
        self.assertEqual(change.origin_value_char, 'A')
        self.assertEqual(change.origin_value_display, 'A')
        change.apply()
        self.assertEqual(change.origin_value_char, 'A')
        self.assertEqual(change.origin_value_display, 'A')
        self.partner.write({'name': 'B'})
        self.assertEqual(change.origin_value_char, 'A')
        self.assertEqual(change.origin_value_display, 'A')

    def test_origin_value_of_change_with_cancel(self):
        """ Origin field is read from the parter or 'old' - with cancel

        According to the state of the change.
        """
        self.partner.with_context(__changeset_rules=True).write({
            'name': 'Y',
        })
        changeset = self.partner.changeset_ids
        change = changeset.change_ids
        self.assertEqual(self.partner.name, 'X')
        self.assertEqual(change.origin_value_char, 'X')
        self.assertEqual(change.origin_value_display, 'X')
        self.partner.write({'name': 'A'})
        self.assertEqual(change.origin_value_char, 'A')
        self.assertEqual(change.origin_value_display, 'A')
        change.cancel()
        self.assertEqual(change.origin_value_char, 'A')
        self.assertEqual(change.origin_value_display, 'A')
        self.partner.write({'name': 'B'})
        self.assertEqual(change.origin_value_char, 'A')
        self.assertEqual(change.origin_value_display, 'A')

    def test_old_field_of_change_with_apply(self):
        """ Old field is stored when the change is applied """
        self.partner.with_context(__changeset_rules=True).write({
            'name': 'Y',
        })
        changeset = self.partner.changeset_ids
        change = changeset.change_ids
        self.assertEqual(self.partner.name, 'X')
        self.assertFalse(change.old_value_char)
        self.partner.write({'name': 'A'})
        self.assertFalse(change.old_value_char)
        change.apply()
        self.assertEqual(change.old_value_char, 'A')
        self.partner.write({'name': 'B'})
        self.assertEqual(change.old_value_char, 'A')

    def test_old_field_of_change_with_cancel(self):
        """ Old field is stored when the change is canceled """
        self.partner.with_context(__changeset_rules=True).write({
            'name': 'Y',
        })
        changeset = self.partner.changeset_ids
        change = changeset.change_ids
        self.assertEqual(self.partner.name, 'X')
        self.assertFalse(change.old_value_char)
        self.partner.write({'name': 'A'})
        self.assertFalse(change.old_value_char)
        change.cancel()
        self.assertEqual(change.old_value_char, 'A')
        self.partner.write({'name': 'B'})
        self.assertEqual(change.old_value_char, 'A')
