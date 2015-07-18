# -*- coding: utf-8 -*-

# Authors: Nemry Jonathan
# Copyright (c) 2014 Acsone SA/NV (http://www.acsone.eu)
# All Rights Reserved
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs.
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contact a Free Software
# Service Company.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

from openerp.tests.common import TransactionCase
from .. import exceptions as ex
import logging
from pprint import pprint, pformat
import traceback
_logger = logging.getLogger(__name__)


class BaseCase(TransactionCase):

    def partner_contact_create(self, lastname, firstname):
        self.original = self.env["res.partner"].create({
            "lastname": lastname,
            "firstname": firstname,
            "is_company": False,
        })
        return self.original

    def partner_company_create(self, name):
        self.original = self.env["res.partner"].create({
            "name": name,
            "is_company": True,
        })
        return self.original

    def user_create(self, lastname, firstname, name=None):
        self.original = self.env["res.users"].create({
            "name": name or u"%s %s" % (self.lastname, self.firstname),
            "login": "firstnametest@example.com",
        })
        return self.original

    def expect(self, lastname, firstname, name=None):
        """Define what is expected in each field when ending."""
        self.lastname = lastname
        self.firstname = firstname
        if name:
            self.name = name
        elif not lastname and firstname:
            self.name = u"%s" % firstname
        elif lastname and not firstname:
            self.name = u"%s" % lastname
        else:
            self.name = u"%s %s" % (lastname, firstname)

        if not hasattr(self, "changed"):
            self.changed = self.original

        for field in ("name", "lastname", "firstname"):
            if getattr(self.changed, field) != getattr(self, field):
                _logger.error('Test failed with wrong ' + pformat(field))
                _logger.error('   self    = ' + pformat(getattr(self, field)))
                _logger.error('   changed = ' + pformat(getattr(self.changed, field)))
            self.assertEqual(
                getattr(self.changed, field),
                getattr(self, field),
                "Test failed with wrong %s" % field)
