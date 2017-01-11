# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from mock import MagicMock
from openerp.tests.common import TransactionCase


class TestResPartner(TransactionCase):

    def setUp(self):
        super(TestResPartner, self).setUp()
        self.partner = self.env['res.partner'].search([
            ('user_ids', '!=', ''),
        ], limit=1)

    def test_action_reset_user_password(self):
        """ It should call user_ids.action_reset_password """
        self.env['res.users']._patch_method(
            'action_reset_password', MagicMock()
        )
        self.partner.action_reset_user_password()
        self.env['res.users'].action_reset_password.assert_called_once()
