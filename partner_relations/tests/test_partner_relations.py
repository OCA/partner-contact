# -*- coding: utf-8 -*-
# Copyright 2015 Camptocamp SA
# Copyright 2016 Therp BV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields
from openerp.tests import common
from openerp.exceptions import ValidationError


class TestPartnerRelation(common.TransactionCase):

    def setUp(self):
        super(TestPartnerRelation, self).setUp()

        self.partner_model = self.env['res.partner']
        self.category_model = self.env['res.partner.category']
        self.type_model = self.env['res.partner.relation.type']
        self.selection_model = self.env['res.partner.relation.type.selection']
        self.relation_model = self.env['res.partner.relation']
        self.relation_all_model = self.env['res.partner.relation.all']
        self.partner_01_person = self.partner_model.create({
            'name': 'Test User 1',
            'is_company': False,
            'ref': 'PR01',
        })
        self.partner_02_company = self.partner_model.create({
            'name': 'Test Company',
            'is_company': True,
            'ref': 'PR02',
        })
        self.type_company2person = self.type_model.create({
            'name': 'mixed',
            'name_inverse': 'mixed_inverse',
            'contact_type_left': 'c',
            'contact_type_right': 'p',
        })
        # Create partners with specific categories:
        self.category_01_ngo = self.category_model.create({
            'name': 'NGO',
        })
        self.partner_03_ngo = self.partner_model.create({
            'name': 'Test NGO',
            'is_company': True,
            'ref': 'PR03',
            'category_id': [(4, self.category_01_ngo.id)],
        })
        self.category_02_volunteer = self.category_model.create({
            'name': 'Volunteer',
        })
        self.partner_04_volunteer = self.partner_model.create({
            'name': 'Test Volunteer',
            'is_company': False,
            'ref': 'PR04',
            'category_id': [(4, self.category_02_volunteer.id)],
        })
        # Determine the two records in res.partner.type.selection that came
        # into existance by creating one res.partner.relation.type:
        selection_types = self.selection_model.search([
            ('type_id', '=', self.type_company2person.id),
        ])
        for st in selection_types:
            if st.is_inverse:
                self.selection_person2company = st
            else:
                self.selection_company2person = st
        assert self.selection_person2company, (
            "Failed to create person to company selection in setup."
        )
        assert self.selection_company2person, (
            "Failed to create company to person selection in setup."
        )
        # Create realion type between NGO and volunteer, and then lookup
        # resulting type_selection_id's:
        self.type_ngo2volunteer = self.type_model.create({
            'name': 'NGO has volunteer',
            'name_inverse': 'volunteer works for NGO',
            'contact_type_left': 'c',
            'contact_type_right': 'p',
            'partner_category_left': self.category_01_ngo.id,
            'partner_category_right': self.category_02_volunteer.id,
        })
        selection_types = self.selection_model.search([
            ('type_id', '=', self.type_ngo2volunteer.id),
        ])
        for st in selection_types:
            if st.is_inverse:
                self.selection_volunteer2ngo = st
            else:
                self.selection_ngo2volunteer = st
        assert self.selection_volunteer2ngo, (
            "Failed to create volunteer to NGO selection in setup."
        )
        assert self.selection_ngo2volunteer, (
            "Failed to create NGO to volunteer selection in setup."
        )

    def test_self_allowed(self):
        """Test creation of relation to same partner when type allows."""
        type_allow = self.type_model.create({
            'name': 'allow',
            'name_inverse': 'allow_inverse',
            'contact_type_left': 'p',
            'contact_type_right': 'p',
            'allow_self': True
        })
        self.relation_model.create({
            'type_id': type_allow.id,
            'left_partner_id': self.partner_01_person.id,
            'right_partner_id': self.partner_01_person.id,
        })

    def test_self_disallowed(self):
        """Test creating relation to same partner when disallowed.

        Attempt to create a relation of a partner to the same partner should
        raise an error when the type of relation explicitly disallows this.
        """
        type_disallow = self.type_model.create({
            'name': 'disallow',
            'name_inverse': 'disallow_inverse',
            'contact_type_left': 'p',
            'contact_type_right': 'p',
            'allow_self': False
        })
        with self.assertRaises(ValidationError):
            self.relation_model.create({
                'type_id': type_disallow.id,
                'left_partner_id': self.partner_01_person.id,
                'right_partner_id': self.partner_01_person.id,
            })

    def test_self_default(self):
        """Test default not to allow relation with same partner.

        Attempt to create a relation of a partner to the same partner
        raise an error when the type of relation does not explicitly allow
        this.
        """
        type_default = self.type_model.create({
            'name': 'default',
            'name_inverse': 'default_inverse',
            'contact_type_left': 'p',
            'contact_type_right': 'p',
        })
        with self.assertRaises(ValidationError):
            self.relation_model.create({
                'type_id': type_default.id,
                'left_partner_id': self.partner_01_person.id,
                'right_partner_id': self.partner_01_person.id,
            })

    def test_self_mixed(self):
        """Test creation of relation with wrong types.

        Trying to create a relation between partners with an inappropiate
        type should raise an error.
        """
        with self.assertRaises(ValidationError):
            self.relation_model.create({
                'type_id': self.type_company2person.id,
                'left_partner_id': self.partner_01_person.id,
                'right_partner_id': self.partner_02_company.id,
            })

    def test_searching(self):
        """Test searching on relations.

        Interaction with the relations should always be through
        res.partner.relation.all.
        """
        relation = self.relation_all_model.create({
            'type_selection_id': self.selection_company2person.id,
            'this_partner_id': self.partner_02_company.id,
            'other_partner_id': self.partner_01_person.id,
        })
        partners = self.partner_model.search([
            ('search_relation_type_id', '=', relation.type_selection_id.id)
        ])
        self.assertTrue(self.partner_02_company in partners)
        partners = self.partner_model.search([
            ('search_relation_type_id', '!=', relation.type_selection_id.id)
        ])
        self.assertTrue(self.partner_01_person in partners)
        partners = self.partner_model.search([
            ('search_relation_type_id', '=', self.type_company2person.name)
        ])
        self.assertTrue(self.partner_01_person in partners)
        self.assertTrue(self.partner_02_company in partners)
        partners = self.partner_model.search([
            ('search_relation_type_id', '=', 'unknown relation')
        ])
        self.assertFalse(partners)
        partners = self.partner_model.search([
            ('search_relation_partner_id', '=', self.partner_02_company.id),
        ])
        self.assertTrue(self.partner_01_person in partners)
        partners = self.partner_model.search([
            ('search_relation_date', '=', fields.Date.today()),
        ])
        self.assertTrue(self.partner_01_person in partners)
        self.assertTrue(self.partner_02_company in partners)

    def test_relation_all(self):
        """Test interactions through res.partner.relation.all."""
        # Check wether we can create connection from company to person,
        # taking the particular company from the active records:
        relation_all_record = self.relation_all_model.with_context(
            active_id=self.partner_02_company.id,
            active_ids=self.partner_02_company.ids,
        ).create({
            'other_partner_id': self.partner_01_person.id,
            'type_selection_id': self.selection_company2person.id,
        })
        # Check wether display name is what we should expect:
        self.assertEqual(
            relation_all_record.display_name, '%s %s %s' % (
                self.partner_02_company.name,
                self.selection_company2person.name,
                self.partner_01_person.name,
            )
        )
        # Check wether the inverse record is present and looks like expected:
        inverse_relation = self.relation_all_model.search([
            ('this_partner_id', '=', self.partner_01_person.id),
            ('other_partner_id', '=', self.partner_02_company.id),
        ])
        self.assertEqual(len(inverse_relation), 1)
        self.assertEqual(
            inverse_relation.type_selection_id.name,
            self.selection_person2company.name
        )
        # Check wether on_change_type_selection works as expected:
        domain = relation_all_record.onchange_type_selection_id()['domain']
        self.assertTrue(
            ('is_company', '=', False) in domain['other_partner_id']
        )
        domain = relation_all_record.onchange_partner_id()['domain']
        self.assertTrue(
            ('contact_type_this', '=', 'c') in domain['type_selection_id']
        )
        relation_all_record.write({
            'type_id': self.type_company2person.id,
        })
        # Check wether underlying record is removed when record is removed:
        relation = relation_all_record.relation_id
        relation_all_record.unlink()
        self.assertFalse(relation.exists())

    def test_symmetric(self):
        """Test creating symmetric relation."""
        # Start out with non symmetric relation:
        type_symmetric = self.type_model.create({
            'name': 'not yet symmetric',
            'name_inverse': 'the other side of not symmetric',
            'is_symmetric': False,
            'contact_type_left': False,
            'contact_type_right': 'p',
        })
        # not yet symmetric relation should result in two records in
        # selection:
        selection_symmetric = self.selection_model.search([
            ('type_id', '=', type_symmetric.id),
        ])
        self.assertEqual(len(selection_symmetric), 2)
        # Now change to symmetric and test name and inverse name:
        with self.env.do_in_draft():
            type_symmetric.write(
                vals={
                    'name': 'sym',
                    'is_symmetric': True,
                }
            )
        with self.env.do_in_onchange():
            type_symmetric.onchange_is_symmetric()
        self.assertEqual(type_symmetric.is_symmetric, True)
        self.assertEqual(
            type_symmetric.name_inverse,
            type_symmetric.name
        )
        self.assertEqual(
            type_symmetric.contact_type_right,
            type_symmetric.contact_type_left
        )
        # now update the database:
        type_symmetric.write(
            vals={
                'name': type_symmetric.name,
                'is_symmetric': type_symmetric.is_symmetric,
                'name_inverse': type_symmetric.name_inverse,
                'contact_type_right': type_symmetric.contact_type_right,
            }
        )
        # symmetric relation should result in only one record in
        # selection:
        selection_symmetric = self.selection_model.search([
            ('type_id', '=', type_symmetric.id),
        ])
        self.assertEqual(len(selection_symmetric), 1)
        relation = self.relation_all_model.create({
            'type_selection_id': selection_symmetric.id,
            'this_partner_id': self.partner_02_company.id,
            'other_partner_id': self.partner_01_person.id,
        })
        partners = self.partner_model.search([
            ('search_relation_type_id', '=', relation.type_selection_id.id)
        ])
        self.assertTrue(self.partner_01_person in partners)
        self.assertTrue(self.partner_02_company in partners)

    def test_category_domain(self):
        """Test check on category in relations."""
        # Check on left side:
        with self.assertRaises(ValidationError):
            self.relation_model.create({
                'type_id': self.type_ngo2volunteer.id,
                'left_partner_id': self.partner_02_company.id,
                'right_partner_id': self.partner_04_volunteer.id,
            })
        # Check on right side:
        with self.assertRaises(ValidationError):
            self.relation_model.create({
                'type_id': self.type_ngo2volunteer.id,
                'left_partner_id': self.partner_03_ngo.id,
                'right_partner_id': self.partner_01_person.id,
            })
        # Creating a relation with a type referring to a certain category
        # should only allow partners for that category.
        relation_all_record = self.relation_all_model.create({
            'this_partner_id': self.partner_03_ngo.id,
            'type_selection_id': self.selection_ngo2volunteer.id,
            'other_partner_id': self.partner_04_volunteer.id,
        })
        # Check wether on_change_type_selection works as expected:
        domain = relation_all_record.onchange_type_selection_id()['domain']
        self.assertTrue(
            ('category_id', 'in', [self.category_01_ngo.id]) in
            domain['this_partner_id']
        )
        self.assertTrue(
            ('category_id', 'in', [self.category_02_volunteer.id]) in
            domain['other_partner_id']
        )

    def test_relation_type_change(self):
        """Test change in relation type conditions."""
        # First create a relation type having no particular conditions.
        type_school2student = self.type_model.create({
            'name': 'school has student',
            'name_inverse': 'studies at school',
        })
        selection_types = self.selection_model.search([
            ('type_id', '=', type_school2student.id),
        ])
        for st in selection_types:
            if st.is_inverse:
                student2school = st
            else:
                school2student = st
        self.assertTrue(school2student)
        self.assertTrue(student2school)
        # Second create relations based on those conditions.
        partner_school = self.partner_model.create({
            'name': 'Test School',
            'is_company': True,
            'ref': 'TS',
        })
        partner_bart = self.partner_model.create({
            'name': 'Bart Simpson',
            'is_company': False,
            'ref': 'BS',
        })
        partner_lisa = self.partner_model.create({
            'name': 'Lisa Simpson',
            'is_company': False,
            'ref': 'LS',
        })
        relation_school2bart = self.relation_all_model.create({
            'type_selection_id': school2student.id,
            'this_partner_id': partner_school.id,
            'other_partner_id': partner_bart.id,
        })
        self.assertTrue(relation_school2bart)
        relation_school2lisa = self.relation_all_model.create({
            'type_selection_id': school2student.id,
            'this_partner_id': partner_school.id,
            'other_partner_id': partner_lisa.id,
        })
        self.assertTrue(relation_school2lisa)
        relation_bart2lisa = self.relation_all_model.create({
            'type_selection_id': school2student.id,
            'this_partner_id': partner_bart.id,
            'other_partner_id': partner_lisa.id,
        })
        self.assertTrue(relation_bart2lisa)
        # Third creata a category and make it a condition for the
        #     relation type.
        # - Test restriction
        # - Test ignore
        category_student = self.category_model.create({
            'name': 'Student',
        })
        with self.assertRaises(ValidationError):
            type_school2student.write({
                'partner_category_right': category_student.id,
            })
        self.assertFalse(type_school2student.partner_category_right.id)
        type_school2student.write({
            'handle_invalid_onchange': 'ignore',
            'partner_category_right': category_student.id,
        })
        self.assertEqual(
            type_school2student.partner_category_right.id,
            category_student.id
        )
        # Fourth make company type a condition for left partner
        # - Test ending
        # - Test deletion
        partner_bart.write({
            'category_id': [(4, category_student.id)],
        })
        partner_lisa.write({
            'category_id': [(4, category_student.id)],
        })
        type_school2student.write({
            'handle_invalid_onchange': 'end',
            'contact_type_left': 'c',
        })
        self.assertEqual(
            relation_bart2lisa.date_end,
            fields.Date.today()
        )
        type_school2student.write({
            'handle_invalid_onchange': 'delete',
            'contact_type_left': 'c',
        })
        self.assertFalse(relation_bart2lisa.exists())
