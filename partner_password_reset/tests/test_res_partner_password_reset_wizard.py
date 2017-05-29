# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from mock import MagicMock
from openerp.exceptions import Warning
from openerp.tests.common import TransactionCase


class TestResPartnerPasswordResetWizard(TransactionCase):

    def test_exception_no_users(self):
        """ It should raise `Warning` when there are no associated users """
        wizard = self.env['res.partner.password.reset.wizard'].with_context(
            active_ids=[]
        )
        with self.assertRaises(Warning):
            wizard.fields_view_get()

    def test_fields_view_get(self):
        """ It should return the wizard correctly """
        partner = self.env.ref('portal.partner_demo_portal')
        wizard = self.env['res.partner.password.reset.wizard'].with_context(
            active_ids=partner.id
        )
        output = wizard.fields_view_get()
        self.assertEquals(output.get('name'), 'Send Password Reset Email')
        self.assertEquals(type(output.get('fields').get('user_ids')), dict)

    def test_action_submit(self):
        """ It should call user_ids.action_reset_password """
        self.env['res.users']._patch_method(
            'action_reset_password', MagicMock()
        )
        partners = self.env.ref('portal.partner_demo_portal')
        wizard = self.env['res.partner.password.reset.wizard'].with_context(
            active_ids=partners.ids
        )
        wizard.action_submit()
        self.env['res.users'].action_reset_password.assert_called_once()
