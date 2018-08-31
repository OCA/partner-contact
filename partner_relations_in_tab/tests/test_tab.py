# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from . import common


class TestTab(common.TestCommon):

    def test_make_field(self):
        self.assertTrue(bool(self.chairperson_tab))
        field = self.chairperson_tab.make_field()
        self.assertEqual(field.string, self.type_has_chairperson.name)
        self.assertEqual(field._obj, 'res.partner.relation')
        self.assertEqual(field._fields_id, 'left_partner_id')
        self.assertEqual(
            field._domain, [('type_id', '=', self.type_has_chairperson.id)])

    def test_get_other_partner_domain(self):
        self.assertTrue(bool(self.chairperson_tab))
        self.assertEqual(
            self.chairperson_tab._get_other_partner_domain(),
            [('is_company', '=', False)])
        self.assertEqual(
            self.is_father_tab._get_other_partner_domain(),
            [('is_company', '=', False),
             ('category_id', 'child_of', self.child_category.id)])

    def test_create_page(self):
        self.assertTrue(bool(self.chairperson_tab))
        page = self.chairperson_tab.create_page()
        # And we should have a field for (amongst others) type_id.
        field = page.xpath('//field[@name="type_id"]')
        self.assertTrue(field, 'Field type_id not in page.')
