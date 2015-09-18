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

from datetime import datetime, timedelta

from openerp import fields, exceptions
from openerp.tests import common
from .common import RevisionMixin


class TestRevisionFlow(RevisionMixin, common.TransactionCase):
    """ Check how revision are generated and applied based on the rules.

    We do not really care about the types of the fields in this test
    suite, so we only use 'char' fields.  We have to ensure that the
    general revision flows work as expected, that is:

    * create a 'done' revision when a manual/system write is made on partner
    * create a revision according to the revision rules when the key
      '__revision_rules' is passed in the context
    * apply a revision change writes the value on the partner
    * apply a whole revision writes all the changes' values on the partner
    * changes in state 'cancel' or 'done' do not write on the partner
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

    def test_new_revision(self):
        """ Add a new revision on a partner

        A new revision is created when we write on a partner with
        ``__revision_rules`` in the context.
        """
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
        self.assertEqual(self.partner.name, 'Y')
        self.assertEqual(self.partner.street, 'street X')
        self.assertEqual(self.partner.street2, 'street2 X')

    def test_new_revision_empty_value(self):
        """ Create a revision change that empty a value """
        self.partner.with_context(__revision_rules=True).write({
            'street': False,
        })
        self.assert_revision(
            self.partner,
            [(self.field_street, 'street X', False, 'draft')]
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
        self.assertEqual(self.partner.name, 'Y')
        self.assertEqual(self.partner.street, 'street Y')
        self.assertEqual(self.partner.street2, 'street2 Y')

    def test_apply_change(self):
        """ Apply a revision change on a partner """
        changes = [
            (self.field_name, 'Y', 'draft'),
        ]
        revision = self._create_revision(self.partner, changes)
        revision.change_ids.apply()
        self.assertEqual(self.partner.name, 'Y')
        self.assertEqual(revision.change_ids.state, 'done')

    def test_apply_done_change(self):
        """ Done changes do not apply (already applied) """
        changes = [
            (self.field_name, 'Y', 'done'),
        ]
        revision = self._create_revision(self.partner, changes)
        revision.change_ids.apply()
        self.assertEqual(self.partner.name, 'X')

    def test_apply_cancel_change(self):
        """ Cancel changes do not apply """
        changes = [
            (self.field_name, 'Y', 'cancel'),
        ]
        revision = self._create_revision(self.partner, changes)
        revision.change_ids.apply()
        self.assertEqual(self.partner.name, 'X')

    def test_apply_empty_value(self):
        """ Apply a change that empty a value """
        changes = [
            (self.field_street, False, 'draft'),
        ]
        revision = self._create_revision(self.partner, changes)
        revision.change_ids.apply()
        self.assertFalse(self.partner.street)

    def test_apply_change_loop(self):
        """ Test @api.multi on the changes """
        changes = [
            (self.field_name, 'Y', 'draft'),
            (self.field_street, 'street Y', 'draft'),
            (self.field_street2, 'street2 Y', 'draft'),
        ]
        revision = self._create_revision(self.partner, changes)
        revision.change_ids.apply()
        self.assertEqual(self.partner.name, 'Y')
        self.assertEqual(self.partner.street, 'street Y')
        self.assertEqual(self.partner.street2, 'street2 Y')

    def test_apply(self):
        """ Apply a full revision on a partner """
        changes = [
            (self.field_name, 'Y', 'draft'),
            (self.field_street, 'street Y', 'draft'),
            (self.field_street2, 'street2 Y', 'draft'),
        ]
        revision = self._create_revision(self.partner, changes)
        revision.apply()
        self.assertEqual(self.partner.name, 'Y')
        self.assertEqual(self.partner.street, 'street Y')
        self.assertEqual(self.partner.street2, 'street2 Y')

    def test_revision_state_on_done(self):
        """ Check that revision state becomes done when changes are done """
        changes = [(self.field_name, 'Y', 'draft')]
        revision = self._create_revision(self.partner, changes)
        self.assertEqual(revision.state, 'draft')
        revision.change_ids.apply()
        self.assertEqual(revision.state, 'done')

    def test_revision_state_on_cancel(self):
        """ Check that rev. state becomes done when changes are canceled """
        changes = [(self.field_name, 'Y', 'draft')]
        revision = self._create_revision(self.partner, changes)
        self.assertEqual(revision.state, 'draft')
        revision.change_ids.cancel()
        self.assertEqual(revision.state, 'done')

    def test_revision_state(self):
        """ Check that revision state becomes done with multiple changes """
        changes = [
            (self.field_name, 'Y', 'draft'),
            (self.field_street, 'street Y', 'draft'),
            (self.field_street2, 'street2 Y', 'draft'),
        ]
        revision = self._create_revision(self.partner, changes)
        self.assertEqual(revision.state, 'draft')
        revision.apply()
        self.assertEqual(revision.state, 'done')

    def test_apply_revision_with_other_pending(self):
        """ Error when applying when previous pending revisions exist """
        changes = [(self.field_name, 'Y', 'draft')]
        old_revision = self._create_revision(self.partner, changes)
        # if the date is the same, both revision can be applied
        to_string = fields.Datetime.to_string
        old_revision.date = to_string(datetime.now() - timedelta(days=1))
        changes = [(self.field_name, 'Z', 'draft')]
        revision = self._create_revision(self.partner, changes)
        with self.assertRaises(exceptions.Warning):
            revision.change_ids.apply()

    def test_apply_different_revisions(self):
        """ Apply different revisions at once """
        partner2 = self.env['res.partner'].create({'name': 'P2'})
        changes = [
            (self.field_name, 'Y', 'draft'),
            (self.field_street, 'street Y', 'draft'),
            (self.field_street2, 'street2 Y', 'draft'),
        ]
        revision = self._create_revision(self.partner, changes)
        revision2 = self._create_revision(partner2, changes)
        self.assertEqual(revision.state, 'draft')
        self.assertEqual(revision2.state, 'draft')
        (revision + revision2).apply()
        self.assertEqual(self.partner.name, 'Y')
        self.assertEqual(self.partner.street, 'street Y')
        self.assertEqual(self.partner.street2, 'street2 Y')
        self.assertEqual(partner2.name, 'Y')
        self.assertEqual(partner2.street, 'street Y')
        self.assertEqual(partner2.street2, 'street2 Y')
        self.assertEqual(revision.state, 'done')
        self.assertEqual(revision2.state, 'done')
