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


class BaseCase(TransactionCase):
    def setUp(self):
        super(BaseCase, self).setUp()
        m_data = self.registry("ir.model.data")
        _, self.company_id = m_data.get_object_reference(
            self.cr, self.uid, "base", "main_company")
        self.company = self.env['res.company'].browse(self.company_id)
        self.counter = 0

    def next_case(self):
        self.counter += 1

    def new_partner(self, is_company):
        new = self.env["res.partner"].new()
        new.is_company = is_company
        new.company_id = self.company_id
        return new

    def partner_contact_create(self, lastname, lastname_second, firstname):
        self.original = self.env["res.partner"].create({
            "lastname": lastname,
            "lastname_second": lastname_second,
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

    def user_create(self, lastname, lastname_second, firstname, name=None):
        data = {"login": "email_%d@example.com" % self.counter}
        if name:
            data["name"] = name
        else:
            data["lastname"] = lastname
            data["lastname_second"] = lastname_second
            data["firstname"] = firstname
        self.original = self.env["res.users"].create(data)
        return self.original

    def _clean_name(self, name, default=False):
        if type(name) in (str, unicode):
            name = u" ".join(name.split(None))
            if not name:
                name = default
        else:
            name = default
        return name

    def _join_names(self, lastname, lastname_second, firstname):
        parts = filter(None, [lastname, lastname_second, firstname])
        return u" ".join(parts)

    def expect(self, lastname, lastname_second, firstname, name=None):
        """Define what is expected in each field when ending."""
        self.lastname = self._clean_name(lastname)
        self.lastname_second = self._clean_name(lastname_second)
        self.firstname = self._clean_name(firstname)
        if name:
            self.name = self._clean_name(name, '')
        else:
            self.name = self._join_names(self.lastname, self.lastname_second,
                                         self.firstname)

        if not hasattr(self, "changed"):
            self.changed = self.original

        for field in ("name", "lastname", "lastname_second", "firstname"):
            self.assertEqual(
                getattr(self.changed, field),
                getattr(self, field),
                "Test case (%d) failed with wrong %s" % (self.counter, field))
