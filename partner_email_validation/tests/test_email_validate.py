# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
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
##############################################################################
from __future__ import unicode_literals

from openerp.tests.common import TransactionCase


class TestEmailValidate(TransactionCase):
    """
    Tests specific reseller behaviors for invoices
    """

    def test_valid_emails(self):
        check = self.registry("res.partner")._check_valid_email
        for email in [
            "mailbox+tag@foo.bar",
            "domain@has-dash.com",
            "hey.I.just.met.y0u@call.me",
            "allô@mail.me",
            "aлrr@test.рф",
            "foo@123.com"
            "the_under@score.com",
        ]:
            self.assertTrue(check(email))

    def test_invalid_emails(self):
        check = self.registry("res.partner")._check_valid_email
        for email in [
            "",
            "noarobas"
            "nodomain@"
            "empty@domain..part",
            "@nomailbox.com"
            "not@fqdn",
            "not@twoletter.c",
            "symbol@in.domain!",
            "s!ymbol@in.mailbox",
        ]:
            self.assertFalse(check(email))
