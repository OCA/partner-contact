# -*- coding: utf-8 -*-
# Copyright 2017 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.addons.partner_multi_relation.tests.test_partner_relation_common \
    import TestPartnerRelationCommon


class TestPartnerMultiRelationParent(TestPartnerRelationCommon):

    # By default it will be false, this makes it run after the modules are
    # installed
    post_install = True

    def count_relations(
            self, this_partner_id=False, type_id=False,
            other_partner_id=False, any_partner_id=False):
        """Count relations satifying criteria passed."""
        domain = []
        if this_partner_id:
            domain.append(('this_partner_id', '=', this_partner_id))
        if type_id:
            domain.append(('type_id', '=', type_id))
        if other_partner_id:
            domain.append(('other_partner_id', '=', other_partner_id))
        if any_partner_id:
            domain.append(('any_partner_id', '=', any_partner_id))
        if not domain:
            return 0
        relation_all_model = self.env['res.partner.relation.all']
        return relation_all_model.search_count(domain)

    def test_address_changes(self):
        """Test wether changes in address are reflected in relations."""
        # make sure that existing contact relation type enabled for sync:
        contact_type = self.env.ref(
            'partner_multi_relation_parent.relation_type_parent_contact'
        )
        contact_type.write({'partner_synchronization_active': True})
        # create a contact for ngo , partner n03
        ngo_contact = self.partner_model.create({
            'name': '03 NGO ACCOUNTANT',
            'is_company': False,
            'ref': 'PR03C01',
            'type': 'contact',
            'parent_id': self.partner_03_ngo.id
        })
        self.assertEqual(
            self.count_relations(
                this_partner_id=ngo_contact.id,
                type_id=contact_type.id,
                other_partner_id=ngo_contact.parent_id.id
            ), 1)
        # then modify partner and verify it
        old_parent_id = ngo_contact.parent_id.id
        ngo_contact.write(
            {'parent_id': self.partner_02_company.id}
        )
        # check no more relations with old_parent
        self.assertEqual(
            self.count_relations(
                this_partner_id=ngo_contact.id,
                type_id=contact_type.id,
                other_partner_id=old_parent_id
            ), 0)
        # check relations are there with current parent
        self.assertEqual(
            self.count_relations(
                this_partner_id=ngo_contact.id,
                type_id=contact_type.id,
                other_partner_id=ngo_contact.parent_id.id
            ), 1)
        # delete NGO ACCOUNTANT
        old_id = ngo_contact.id
        old_parent_id = ngo_contact.parent_id.id
        ngo_contact.unlink()
        self.assertEqual(
            self.count_relations(
                this_partner_id=old_id,
                type_id=contact_type.id,
                other_partner_id=old_parent_id
            ), 0)

    def test_relation_type_changes(self):
        """Test wether changes in address are reflected in relations."""
        # make sure that existing delivery relation type NOT enabled for sync:
        delivery_type = self.env.ref(
            'partner_multi_relation_parent.relation_type_parent_delivery'
        )
        delivery_type.write({'partner_synchronization_active': False})
        # create a delivery address for ngo , partner n03
        ngo_delivery = self.partner_model.create({
            'name': '03 NGO Delivery Address',
            'is_company': False,
            'ref': 'PR03D01',
            'type': 'delivery',
            'parent_id': self.partner_03_ngo.id
        })
        self.assertEqual(
            self.count_relations(
                this_partner_id=ngo_delivery.id,
                type_id=delivery_type.id,
                other_partner_id=ngo_delivery.parent_id.id
            ), 0)
        # after enabling delivery relation type, relations should be there:
        delivery_type.write({'partner_synchronization_active': True})
        self.assertEqual(
            self.count_relations(
                this_partner_id=ngo_delivery.id,
                type_id=delivery_type.id,
                other_partner_id=ngo_delivery.parent_id.id
            ), 1)

    def test_relation_changes(self):
        """Test wether changes in relation are reflected in address.

        NB: left partner is the address partner, right partner the parent.
        """
        # make sure that existing contact relation type enabled for sync:
        contact_type = self.env.ref(
            'partner_multi_relation_parent.relation_type_parent_contact')
        contact_type.write({'partner_synchronization_active': True})
        # create a contact address, to be linked to ngo partner:
        ngo_contact = self.partner_model.create({
            'name': '03 NGO ACCOUNTANT',
            'is_company': False,
            'ref': 'PR03C01',
        })
        # Now create a contact address relation:
        ngo_relation = self.relation_all_model.create({
            'this_partner_id': ngo_contact.id,
            'type_id': contact_type.id,
            'other_partner_id': self.partner_03_ngo.id})
        # Now the contact address should be linked to parent as contact:
        self.assertEqual(ngo_contact.parent_id.name, self.partner_03_ngo.name)
        self.assertEqual(ngo_contact.type, 'contact')
        # Now link the contact address to another company:
        old_parent_id = ngo_contact.parent_id.id
        ngo_relation.write({'other_partner_id': self.partner_02_company.id})
        # check no more relations with old_parent
        self.assertEqual(
            self.count_relations(
                this_partner_id=ngo_contact.id,
                other_partner_id=old_parent_id), 0)
        # check relations are there with current parent
        self.assertEqual(
            self.count_relations(
                this_partner_id=ngo_contact.id,
                other_partner_id=ngo_contact.parent_id.id), 1)
        # Remove the relation altoghether:
        old_parent_id = ngo_contact.parent_id.id
        ngo_relation.unlink()
        self.assertEqual(
            self.count_relations(
                this_partner_id=ngo_contact.id,
                other_partner_id=old_parent_id), 0)
        self.assertEqual(ngo_contact.parent_id.id, False)
