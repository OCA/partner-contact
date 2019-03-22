# Copyright 2017-2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import exceptions
from odoo.tests import common


class TestPartnerDeduplicateAcl(common.TransactionCase):
    def setUp(self):
        super(TestPartnerDeduplicateAcl, self).setUp()
        self.partner_1 = self.env['res.partner'].create({
            'name': 'Partner 1',
            'email': 'partner1@example.org',
            'is_company': True,
            'parent_id': False,
        })
        self.partner_2 = self.partner_1.copy()
        self.partner_2.write({
            'name': 'Partner 1',
            'email': 'partner2@example.org'
        })
        self.user = self.env['res.users'].create({
            'login': 'test_crm_deduplicate_acl',
            'name': 'test_crm_deduplicate_acl',
            'email': 'partner_deduplicate_acl@example.org',
            'groups_id': [
                (4, self.env.ref('base.group_user').id),
                (4, self.env.ref('base.group_partner_manager').id),
            ]
        })
        self.wizard = self.env['base.partner.merge.automatic.wizard'].sudo(
            self.user,
        ).create({
            'group_by_name': True,
        })

    def test_same_email_restriction(self):
        self.wizard.action_start_manual_process()
        with self.assertRaises(exceptions.UserError):
            self.wizard.action_merge()
        self.user.groups_id = [
            (4, self.env.ref('partner_deduplicate_acl.group_unrestricted').id),
        ]
        # Now there shouldn't be error
        self.wizard.action_merge()
