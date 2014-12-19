# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2010 - 2014 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
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

from openerp.tests.common import TransactionCase


class test_partner_contact_id(TransactionCase):

    def setUp(self):
        super(test_partner_contact_id, self).setUp()
        # Clean up registries
        self.registry('ir.model').clear_caches()
        self.registry('ir.model.data').clear_caches()
        # Get registries
        self.user_model = self.registry("res.users")
        self.partner_model = self.registry("res.partner")
        # Get context
        self.context = self.user_model.context_get(self.cr, self.uid)
        # Create values for test, contact also created
        contact_id = self.partner_model.create(self.cr, self.uid, {
            'name': u'Astérix',
            'title': 1,
        }, context=self.context)
        self.vals = {
            'name': u'Obélix',
            'type': 'contact',
            'contact_id': contact_id,
        }

    def test_create_partner(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        partner_id = self.partner_model.create(cr, uid, vals, context=context)
        partner = self.partner_model.browse(
            cr, uid, partner_id, context=context
        )
        # Creating the partner uses the name from the contact
        self.assertEqual(partner.name, u'Astérix')
        self.assertEqual(partner.lastname, u'Astérix')
