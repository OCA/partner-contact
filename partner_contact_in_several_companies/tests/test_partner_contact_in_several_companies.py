# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, SUPERUSER_ID
from odoo.tests import common


class PartnerContactInSeveralCompaniesCase(common.TransactionCase):

    def setUp(self):
        """*****setUp*****"""
        super(PartnerContactInSeveralCompaniesCase, self).setUp()
        cr, uid = self.cr, self.uid
        env = api.Environment(cr, SUPERUSER_ID, {})
        ModelData = env['ir.model.data']
        self.partner = env['res.partner']
        self.action = env['ir.actions.act_window']

        # Get test records reference
        for attr, module, name in [
                ('main_partner_id', 'base', 'main_partner'),
                ('bob_contact_id',
                 'partner_contact_in_several_companies',
                 'res_partner_contact1'),
                ('bob_job1_id',
                 'partner_contact_in_several_companies',
                 'res_partner_contact1_work_position1'),
                ('roger_contact_id', 'base', 'res_partner_main2'),
                ('roger_job2_id',
                 'partner_contact_in_several_companies',
                 'res_partner_main2_position_consultant'),
                ('base_partner_action_id', 'base', 'action_partner_form'),
                ('custom_partner_action_id',
                 'partner_contact_in_several_companies',
                 'action_partner_form'),
                ]:
            r = ModelData.get_object_reference(module, name)
            setattr(self, attr, r[1] if r else False)

    def test_00_show_only_standalone_contact(self):
        """Check that only standalone contact are shown if context
        explicitly state to not display all positions
        """
        cr, uid = self.cr, self.uid
        ctx = {'search_show_all_positions': {'is_set': True,
                                             'set_value': False
                                             }}
        partner_ids = self.partner.search([])
        partner_ids.sort()
        self.assertTrue(self.bob_job1_id not in partner_ids)
        self.assertTrue(self.roger_job2_id not in partner_ids)

    def test_01_show_all_positions(self):
        """Check that all contact are show if context is empty or
        explicitly state to display all positions or the "is_set"
        value has been set to False.
        """

        partner_ids = self.partner.search([])
        self.assertTrue(self.bob_job1_id in partner_ids)
        self.assertTrue(self.roger_job2_id in partner_ids)

        ctx = {'search_show_all_positions': {'is_set': False}}
        partner_ids = self.partner.search([])
        self.assertTrue(self.bob_job1_id in partner_ids)
        self.assertTrue(self.roger_job2_id in partner_ids)

        ctx = {'search_show_all_positions': {'is_set': True,
                                             'set_value': True
                                             }}
        partner_ids = self.partner.search([])
        self.assertTrue(self.bob_job1_id in partner_ids)
        self.assertTrue(self.roger_job2_id in partner_ids)

    def test_02_reading_other_contact_one2many_show_all_positions(self):
        """Check that readonly partner's ``other_contact_ids`` return
        all values whatever the context
        """

        def read_other_contacts(pid, context=None):
            return self.partner.read(
                [pid], ['other_contact_ids'])[0]['other_contact_ids']

        def read_contacts(pid, context=None):
            return self.partner.read(
                [pid], ['child_ids'])[0]['child_ids']

        ctx = None
        self.assertEqual(
            read_other_contacts(self.bob_contact_id, context=ctx),
            [self.bob_job1_id],
        )
        ctx = {'search_show_all_positions': {'is_set': False}}
        self.assertEqual(read_other_contacts(
            self.bob_contact_id),
            [self.bob_job1_id],
        )
        ctx = {'search_show_all_positions': {'is_set': True,
                                             'set_value': False
                                             }}
        self.assertEqual(read_other_contacts(
            self.bob_contact_id,),
            [self.bob_job1_id],
        )
        ctx = {'search_show_all_positions': {'is_set': True,
                                             'set_value': True
                                             }}
        self.assertEqual(
            read_other_contacts(self.bob_contact_id),
            [self.bob_job1_id],
        )

        ctx = None
        self.assertIn(
            self.bob_job1_id,
            read_contacts(self.main_partner_id),
        )
        ctx = {'search_show_all_positions': {'is_set': False}}
        self.assertIn(
            self.bob_job1_id,
            read_contacts(self.main_partner_id),
        )
        ctx = {'search_show_all_positions': {'is_set': True,
                                             'set_value': False
                                             }}
        self.assertIn(
            self.bob_job1_id,
            read_contacts(self.main_partner_id),
        )
        ctx = {'search_show_all_positions': {'is_set': True,
                                             'set_value': True
                                             }}
        self.assertIn(
            self.bob_job1_id,
            read_contacts(self.main_partner_id),
        )

    def test_03_search_match_attached_contacts(self):
        """Check that searching partner also return partners having
        attached contacts matching search criteria
        """
        # Bob's contact has one other position which is related to
        # 'YourCompany'
        # so search for all contacts working for 'YourCompany'
        # should contain Bob position.
        partner_ids = self.partner.search(
            [('parent_id', 'ilike', 'YourCompany')])
        self.assertIn(self.bob_job1_id, partner_ids, )

        # but when searching without 'all positions',
        # we should get the position standalone contact instead.
        ctx = {'search_show_all_positions': {'is_set': True,
                                             'set_value': False
                                             }}
        partner_ids = self.partner.search(
            [('parent_id', 'ilike', 'YourCompany')])
        self.assertIn(self.bob_contact_id, partner_ids, )

    def test_04_contact_creation(self):
        """Check that we're begin to create a contact"""

        # Create a contact using only name
        new_contact_id = self.partner.create({'name': 'Bob Egnops'})
        self.assertEqual(
            self.partner.browse(cr, uid, new_contact_id).contact_type,
            'standalone',
        )

        # Create a contact with only contact_id
        new_contact_id = self.partner.create(
            {'contact_id': self.bob_contact_id}
        )
        new_contact = self.partner.browse(new_contact_id)
        self.assertEqual(new_contact.name, 'Bob Egnops')
        self.assertEqual(new_contact.contact_type, 'attached')

        # Create a contact with both contact_id and name;
        # contact's name should override provided value in that case
        new_contact_id = self.partner.create(
            {'contact_id': self.bob_contact_id, 'name': 'Rob Egnops'}
        )
        self.assertEqual(
            new_contact_id.name,
            'Bob Egnops'
        )

        # Reset contact to standalone
        new_contact_id.write({'contact_id': False})
        self.assertEqual(
            new_contact_id.contact_type,
            'standalone',
        )

        # Reset contact to attached, and ensure only it is unlinked (i.e.
        # context is ignored).
        new_contact_id.write([
                           {'contact_id': self.bob_contact_id})
        ctx = {'search_show_all_positions': {'is_set': True,
                                             'set_value': True
                                             }}
        new_contact_id.with_context(ctx).unlink()
        partner_ids = self.partner.search(
            [('id', 'in', [new_contact_id, self.bob_contact_id])])
        self.assertIn(self.bob_contact_id, partner_ids)
        self.assertNotIn(new_contact_id, partner_ids)

    def test_05_contact_fields_sync(self):
        """Check that contact's fields are correctly synced between
        parent contact or related contacts
        """

        # Test DOWNSTREAM sync
        self.bob_contact_id.write(
            {'name': 'Rob Egnops'}
        )
        self.assertEqual(
            self.partner.browse(self.bob_job1_id).name,
            'Rob Egnops',
        )

        # Test UPSTREAM sync
        self.bob_job1_id.write({'name': 'Bob Egnops'})
        self.assertEqual(
            self.partner.browse(self.bob_contact_id).name,
            'Bob Egnops',
        )

    def test_06_ir_action(self):
        """Check ir_action context is auto updated.
        """

        new_context_val = "'search_show_all_positions': " \
            "{'is_set': True, 'set_value': False},"

        details = self.action.read(
            [self.base_partner_action_id]
        )
        self.assertIn(
            new_context_val,
            details[0]['context'],
            msg='Default actions not updated with new context'
        )

        details = self.action.read(
            [self.custom_partner_action_id]
        )
        self.assertNotIn(
            new_context_val,
            details[0]['context'],
            msg='Custom actions incorrectly updated with new context'
        )
