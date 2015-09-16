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
from .common import RevisionMixin


class TestRevisionFlow(RevisionMixin, common.TransactionCase):
    """ Check how revision are generated and applied based on the rules.

    We do not really care about the types of the fields in this test suite,
    but we have to ensure that the general revision flows work as expected.
    """

    def _setup_behavior(self):
        RevisionBehavior = self.env['revision.behavior']
        partner_model_id = self.env.ref('base.model_res_partner').id
        self.field_name = self.env.ref('base.field_res_partner_name')
        self.field_street = self.env.ref('base.field_res_partner_street')
        self.field_street2 = self.env.ref('base.field_res_partner_street2')
        RevisionBehavior.create({
            'model_id': partner_model_id,
            'field_id': self.field_name.id,
            'default_behavior': 'auto',
        })
        RevisionBehavior.create({
            'model_id': partner_model_id,
            'field_id': self.field_street.id,
            'default_behavior': 'validate',
        })
        RevisionBehavior.create({
            'model_id': partner_model_id,
            'field_id': self.field_street2.id,
            'default_behavior': 'never',
        })

    def setUp(self):
        super(TestRevisionFlow, self).setUp()
        self._setup_behavior()
        self.partner = self.env['res.partner'].create({
            'name': 'X',
            'street': 'street X',
            'street2': 'street2 X',
        })

    def assert_revision(self, partner, expected_changes):
        """ Check if a revision has been created according to expected values

        The partner should have no prior revision than the one created in the
        test (so it has exactly 1 revision).

        The expected changes are tuples with (field, current_value,
        new_value, state)

        :param partner: record of partner having a revision
        :param expected_changes: contains tuples with the changes
        :type expected_changes: list(tuple))
        """
        revision = self.env['res.partner.revision'].search(
            [('partner_id', '=', partner.id)],
        )
        self.assertEqual(len(revision), 1,
                         "1 revision expected, got %s" % (revision,))
        changes = revision.change_ids
        missing = []
        for expected_change in expected_changes:
            for change in changes:
                if (change.field_id, change.current_value, change.new_value,
                        change.state) == expected_change:
                    changes -= change
                    break
            else:
                missing.append(expected_change)
        message = u''
        for field, current_value, new_value, state in missing:
            message += ("- field: '%s', current_value: '%s', "
                        "new_value: '%s', state: '%s'\n" %
                        (field.name, current_value, new_value, state))
        for change in changes:
            message += ("+ field: '%s', current_value: '%s', "
                        "new_value: '%s', state: '%s'\n" %
                        (change.field_id.name, change.current_value,
                         change.new_value, change.state))
        if message:
            raise AssertionError('Changes do not match\n\n:%s' % message)

    def test_new_revision(self):
        """ Add a new revision on a partner """
        self.partner.with_context(__revision_rules=True).write({
            'name': 'Y',
            'street': 'street Y',
            'street2': 'street2 Y',
        })
        self.assert_revision(
            self.partner,
            [(self.field_name, 'X', 'Y', 'done'),
             (self.field_street, 'street X', 'street Y', 'draft'),
             (self.field_street2, 'street2 X', 'street2 Y', 'cancel'),
             ],
        )

    def test_manual_edition(self):
        """ A manual edition of a partner should always be applied

        But should create a 'done' revision
        """
        self.partner.write({
            'name': 'Y',
            'street': 'street Y',
            'street2': 'street2 Y',
        })
        self.assert_revision(
            self.partner,
            [(self.field_name, 'X', 'Y', 'done'),
             (self.field_street, 'street X', 'street Y', 'done'),
             (self.field_street2, 'street2 X', 'street2 Y', 'done'),
             ],
        )
