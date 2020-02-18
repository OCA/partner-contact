# -*- coding: utf-8 -*-
# Copyright 2014-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from . import common


class TestResPartnerRelation(common.TestCommon):

    def test_relations(self):
        """Test relations shown on tab."""
        self.assertTrue(bool(self.chairperson_tab))
        big_company = self._make_partner({
            'name': 'Big company',
            'is_company': True,
            'ref': 'BIG'})
        important_person = self._make_partner({
            'name': 'Bart Simpson',
            'is_company': False,
            'ref': 'BS'})
        relation_company_chair = self._make_relation({
            'left_partner_id': big_company.id,
            'type_id': self.type_has_chairperson.id,
            'right_partner_id': important_person.id})
        # We should find the chairperson of the company through the tab:
        fieldname = self.chairperson_tab.get_fieldname()
        executive_relations = big_company[fieldname]
        self.assertEqual(len(executive_relations), 1)
        self.assertEqual(
            executive_relations[0].id, relation_company_chair.id)
        self.assertEqual(
            executive_relations[0].right_partner_id.id, important_person.id)
