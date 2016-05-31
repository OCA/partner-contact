# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests.common import TransactionCase


class TestPartnerContactGender(TransactionCase):
    def test_partner_contact_gender(self):
        from ..hooks import post_init_hook
        post_init_hook(self.cr, None)
