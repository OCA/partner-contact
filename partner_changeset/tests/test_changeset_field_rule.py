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


class TestChangesetFieldRule(common.TransactionCase):

    def setUp(self):
        super(TestChangesetFieldRule, self).setUp()
        self.partner_model_id = self.env.ref('base.model_res_partner').id
        self.field_name = self.env.ref('base.field_res_partner_name')
        self.field_street = self.env.ref('base.field_res_partner_street')

    def test_get_rules(self):
        ChangesetFieldRule = self.env['changeset.field.rule']
        rule1 = ChangesetFieldRule.create({
            'model_id': self.partner_model_id,
            'field_id': self.field_name.id,
            'action': 'validate',
        })
        rule2 = ChangesetFieldRule.create({
            'model_id': self.partner_model_id,
            'field_id': self.field_street.id,
            'action': 'never',
        })
        get_rules = ChangesetFieldRule.get_rules('res.partner')
        self.assertEqual(get_rules, {'name': rule1, 'street': rule2})

    def test_get_rules_cache(self):
        ChangesetFieldRule = self.env['changeset.field.rule']
        rule = ChangesetFieldRule.create({
            'model_id': self.partner_model_id,
            'field_id': self.field_name.id,
            'action': 'validate',
        })
        self.assertEqual(
            ChangesetFieldRule.get_rules('res.partner')['name'].action,
            'validate',
        )
        # Write on cursor to bypass the cache invalidation for the
        # matter of the test
        self.env.cr.execute("UPDATE changeset_field_rule "
                            "SET action = 'never' "
                            "WHERE id = %s", (rule.id,))
        self.assertEqual(
            ChangesetFieldRule.get_rules('res.partner')['name'].action,
            'validate',
        )
        rule.action = 'auto'
        self.assertEqual(
            ChangesetFieldRule.get_rules('res.partner')['name'].action,
            'auto',
        )
        rule.unlink()
        self.assertFalse(ChangesetFieldRule.get_rules('res.partner'))
