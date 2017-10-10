# -*- coding: utf-8 -*-
# Copyright 2017 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.addons.partner_multi_relation.tests.test_partner_relation_common \
    import TestPartnerRelationCommon


class TestPartnerMultiRelationParent(TestPartnerRelationCommon):
    # pylint: disable=invalid-name
    def setUp(self):
        super(TestPartnerMultiRelationParent, self).setUp()
        self.par_rel_mod = self.env['res.partner.relation']
        self.type_relation = self.env.ref(
            'partner_multi_relation_parent.parent_relation_type'
        ).id

    # By default it will be false, this makes it run after the modules are
    # installed
    post_install = True

    def count_partner_relation_left_right(self, partner_id, parent_id=None):
        # returns number relations , should be always 1
        # todo extend this with relations_all  calculations (left, right)
        if not parent_id:
            return 0
        hits = self.par_rel_mod.search([
            ('left_partner_id', '=', partner_id),
            ('type_id', '=', self.type_relation),
            ('right_partner_id', '=', parent_id)
        ])
        return len(hits)

    def count_relations_of_parent(self, parent_id):
        hits = self.par_rel_mod.search([
            ('type_id', '=', self.type_relation),
            ('right_partner_id', '=', parent_id)
        ])
        return len(hits)

    def test_partner_multi_relation_parent(self):
        # verify that existing partners do have relations
        relations = self.count_partner_relation_left_right(
            self.partner_01_person.id, self.partner_01_person.parent_id.id
        )
        self.assertEqual(relations, 0)
        # create a contact for ngo , partner n03
        ngo_contact = self.partner_model.create({
            'name': '03 NGO ACCOUNTANT',
            'is_company': False,
            'ref': 'PR03C01',
            'parent_id': self.partner_03_ngo.id
        })
        relations = self.count_partner_relation_left_right(
            ngo_contact.id, ngo_contact.parent_id.id
        )
        self.assertEqual(relations, 1)
        # then modify partner and verify it
        old_parent = ngo_contact.parent_id.id
        ngo_contact.write(
            {'parent_id': self.partner_02_company.id}
        )
        # check no more relations with old_parent
        relations = self.count_partner_relation_left_right(
            ngo_contact.id, old_parent
        )
        self.assertEqual(relations, 0)
        # check relations are there with current parent

        relations = self.count_partner_relation_left_right(
            ngo_contact.id, ngo_contact.parent_id.id
        )
        self.assertEqual(relations, 1)
        # delete NGO ACCOUNTANT
        old_id = ngo_contact.id
        old_parent_id = ngo_contact.parent_id.id
        ngo_contact.unlink()

        relations = self.count_partner_relation_left_right(
            old_id, old_parent_id
        )
        self.assertEqual(relations, 0)
        # test with multiple contacts
        # 15 for ngo and 15 for company
        for partners in range(30):
            if partners % 2 == 0:
                self.partner_model.create({
                    'name': '03 NGO %s' % str(partners),
                    'is_company': False,
                    'ref': 'PR03C%s' % str(partners),
                    'parent_id': self.partner_03_ngo.id
                })
                continue
            self.partner_model.create({
                'name': '02 Company %s' % str(partners),
                'is_company': False,
                'ref': 'PR02C%s' % str(partners),
                'parent_id': self.partner_02_company.id
            })
        # try to delete the has contact type , forbade
        contact_relations = self.count_relations_of_parent(
            self.partner_02_company.id
        )
        self.assertEqual(contact_relations, 15)
