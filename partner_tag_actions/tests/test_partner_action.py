# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Savoir-faire Linux
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

from openerp.tests import TransactionCase


class PartnerActionTest(TransactionCase):
    """
    Tests tweaks to res.partner: defaults and case modifications
    """
    def setUp(self):
        super(PartnerActionTest, self).setUp()
        self.partner_obj = self.env["res.partner"]
        self.cat_obj = self.env["res.partner.category"]
        self.action_obj = self.env["partner.action"]
        self.action_type_obj = self.env["partner.action.type"]

        self.partner = self.partner_obj.create({
            "name": "Monty Python",
        })
        self.tag_a = self.cat_obj.create({"name": "Tag A"})
        self.tag_b = self.cat_obj.create({"name": "Tag B"})

    def test_create_done(self):
        """ Test that tags are applied when creating """
        add_a = self.action_type_obj.create({
            "name": "Add A",
            "add_tag": self.tag_a.id,
        })
        self.action_obj.create({
            "partner_id": self.partner.id,
            "state": "done",
            "action_type": add_a.id,
        })
        self.assertIn(
            self.tag_a,
            self.partner.category_id,
            "Partner should have gotten Tag A")

    def test_create_and_done(self):
        """ Test that tags are applied when changing their state """
        add_a = self.action_type_obj.create({
            "name": "Add A",
            "add_tag": self.tag_a.id,
        })
        action = self.action_obj.create({
            "partner_id": self.partner.id,
            "state": "draft",
            "action_type": add_a.id,
        })
        self.assertNotIn(
            self.tag_a,
            self.partner.category_id,
            "Partner should not have gotten Tag A")

        action.write({"state": 'done'})

        self.assertIn(
            self.tag_a,
            self.partner.category_id,
            "Partner should have gotten Tag A")

    def test_01_priority(self):
        """ Test that tags are applied by their priority """
        add_a = self.action_type_obj.create({
            "name": "Add A, Del B",
            "add_tag": self.tag_a.id,
            "remove_tag": self.tag_b.id,
            "priority": 10,
        })

        add_b = self.action_type_obj.create({
            "name": "Add B, Del A",
            "add_tag": self.tag_b.id,
            "remove_tag": self.tag_a.id,
            "priority": 0,
        })
        self.action_obj.create({
            "partner_id": self.partner.id,
            "state": 'done',
            "action_type": add_b.id,
        })
        self.action_obj.create({
            "partner_id": self.partner.id,
            "state": 'done',
            "action_type": add_a.id,
        })

        self.assertNotIn(
            self.tag_a,
            self.partner.category_id,
            "Partner should not have gotten Tag A")

        self.assertIn(
            self.tag_b,
            self.partner.category_id,
            "Partner should have gotten Tag B")
