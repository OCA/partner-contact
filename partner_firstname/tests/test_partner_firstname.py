# -*- coding: utf-8 -*-
##############################################################################
#
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
#
##############################################################################
import openerp.tests.common as common

from openerp.tools.translate import _


class test_partner_firstname(common.TransactionCase):

    def setUp(self):
        super(test_partner_firstname, self).setUp()

        self.registry('ir.model').clear_caches()
        self.registry('ir.model.data').clear_caches()

        self.user_model = self.registry("res.users")
        self.partner_model = self.registry("res.partner")
        self.fields_partner = {
            'lastname': 'lastname',
            'firstname': 'firstname',
        }
        self.fields_user = {
            'name': 'lastname',
            'login': 'v5Ue4Tql0Pm67KX05g25A',
        }

        self.context = self.user_model.context_get(self.cr, self.uid)

    def test_copy_partner(self):
        cr, uid, context = self.cr, self.uid, self.context
        res_id = self.partner_model.create(
            cr, uid, self.fields_partner, context=context
        )
        res_id = self.partner_model.copy(
            cr, uid, res_id, default={}, context=context
        )
        vals = self.partner_model.read(
            cr, uid, [res_id],
            ['name', 'lastname', 'firstname'], context=context
        )[0]

        self.assertEqual(
            vals['name'],
            _('%s (copy)') % 'lastname' + " firstname",
            'Copy of the partner failed with wrong name'
        )
        self.assertEqual(
            vals['lastname'],
            _('%s (copy)') % 'lastname',
            'Copy of the partner failed with wrong lastname'
        )
        self.assertEqual(
            vals['firstname'],
            'firstname',
            'Copy of the partner failed with wrong firstname'
        )

    def test_copy_user(self):
        cr, uid, context = self.cr, self.uid, self.context
        # create a user
        res_id = self.user_model.create(
            cr, uid, self.fields_user, context=context
        )
        # get the related partner id and add it a firstname
        flds = self.user_model.read(
            cr, uid, [res_id], ['partner_id'], context=context
        )[0]
        self.partner_model.write(
            cr, uid, flds['partner_id'][0], {'firstname': 'firstname'},
            context=context
        )
        # copy the user and compare result
        res_id = self.user_model.copy(
            cr, uid, res_id, default={}, context=context
        )
        vals = self.user_model.read(
            cr, uid, [res_id], ['name', 'lastname', 'firstname'],
            context=context
        )[0]

        self.assertEqual(
            vals['name'],
            _('%s (copy)') % 'lastname' + ' firstname',
            'Copy of the user failed with wrong name'
        )
        self.assertEqual(
            vals['lastname'],
            _('%s (copy)') % 'lastname',
            'Copy of the user failed with wrong lastname'
        )
        self.assertEqual(
            vals['firstname'],
            'firstname',
            'Copy of the user failed with wrong firstname'
        )

    def test_update_user_lastname(self):
        cr, uid, context = self.cr, self.uid, self.context
        # create a user
        res_id = self.user_model.create(
            cr, uid, self.fields_user, context=context
        )
        # get the related partner id and add it a firstname
        flds = self.user_model.read(
            cr, uid, [res_id], ['partner_id'], context=context
        )[0]
        self.partner_model.write(
            cr, uid, flds['partner_id'][0], {'firstname': 'firstname'},
            context=context
        )
        self.user_model.write(
            cr, uid, res_id, {'name': 'change firstname'}, context=context
        )
        vals = self.user_model.read(
            cr, uid, [res_id], ['name', 'lastname', 'firstname'],
            context=context
        )[0]

        self.assertEqual(
            vals['name'],
            'change firstname',
            'Update of the user lastname failed with wrong name'
        )
        self.assertEqual(
            vals['lastname'],
            'change',
            'Update of the user lastname failed with wrong lastname'
        )
        self.assertEqual(
            vals['firstname'],
            'firstname',
            'Update of the user lastname failed with wrong firstname'
        )

    def test_update_user_firstname(self):
        cr, uid, context = self.cr, self.uid, self.context
        # create a user
        res_id = self.user_model.create(
            cr, uid, self.fields_user, context=context
        )
        # get the related partner id and add it a firstname
        flds = self.user_model.read(
            cr, uid, [res_id], ['partner_id'], context=context
        )[0]
        self.partner_model.write(
            cr, uid, flds['partner_id'][0], {'firstname': 'firstname'},
            context=context
        )
        self.user_model.write(
            cr, uid, res_id, {'name': 'lastname other'}, context=context
        )
        vals = self.user_model.read(
            cr, uid, [res_id], ['name', 'lastname', 'firstname'],
            context=context
        )[0]

        self.assertEqual(
            vals['name'],
            'lastname other',
            'Update of the user firstname failed with wrong name'
        )
        self.assertEqual(
            vals['lastname'],
            'lastname other',
            'Update of the user firstname failed with wrong lastname'
        )
        self.assertFalse(
            vals['firstname'],
            'Update of the user firstname failed with wrong firstname'
        )

    def test_create_user_login_only(self):
        """Test creation of a user with only the login supplied"""
        cr, uid, context = self.cr, self.uid, self.context
        # create a user
        res_id = self.user_model.create(
            cr, uid, {'login': 'test_login_only'}, context=context
        )
        # get the related partner id and add it a firstname
        user = self.user_model.browse(cr, uid, res_id, context=context)
        self.assertEqual(user.login, user.name)
        self.assertEqual(user.login, user.lastname)
        self.assertEqual(user.login, user.partner_id.lastname)
