from odoo.tests import common


class TestPartnerAffiliate(common.TransactionCase):

    def setUp(self):
        super(TestPartnerAffiliate, self).setUp()
        self.partner_obj = self.env['res.partner']

        self.first_company = self.partner_obj.create({
            'name': 'MyFirstCompanyForTheAffiliate',
            'type': 'contact',
            'is_company': True,
            'street': 'first company street',
        })

        self.second_company = self.partner_obj.create({
            'name': 'MySecondCompanyForTheAffiliate',
            'type': 'contact',
            'is_company': True,
            'street': 'second company street',
        })

    # Check data integrity of the objects when an affiliate is given a new
    # parent. So both objects keeps their data.
    def test_change_parent_from_a_new_affiliate(self):
        my_affiliate = self.partner_obj.create({
            'name': 'MyAffiliate',
            'is_company': True,
            'parent_id': self.first_company.id,
            'type': 'affiliate',
            'street': 'affiliate street',
        })

        # Checks for data integrity in affiliate and his parent.
        self.assertTrue(my_affiliate, "The new affiliate have been created.")

        self.assertEquals(my_affiliate.type, 'affiliate',
                          "Check type must be 'affiliate'")
        self.assertEquals(my_affiliate.parent_id.id, self.first_company.id,
                          "Must be child of the parent defined in the setup")
        self.assertEquals(my_affiliate.street, "affiliate street",
                          "The street have been correctly set.")
        self.assertEquals(self.first_company.street, "first company street",
                          "The parent continues with his original street")

        # Change the parent of the affiliate for the second one in the set-up.
        my_affiliate.parent_id = self.second_company.id
        my_affiliate.onchange_parent_id()

        # The parent have been changed. And is not the first one.
        self.assertEquals(my_affiliate.parent_id.id, self.second_company.id)

        # The affiliate keeps its data for the street (address). Not modified.
        self.assertEquals(my_affiliate.street, "affiliate street",
                          "keeps the same street")
        # The data for the street of the first parent have not been changed.
        self.assertEquals(self.first_company.street, "first company street",
                          "keeps the same street")

    # Check that the default value for 'type' defined by default in the view
    # is set correctly when a new affiliate is created.
    def test_new_affiliate_is_created_with_type_affiliate_by_default(self):
        new_affiliate = self.partner_obj.with_context(
            {'default_parent_id': self.first_company.id,
             'default_is_company': True,
             'default_type': 'affiliate'
             }
        ).create({
            'name': 'MyTestAffiliate',
            'street': 'affiliate street',
        })

        self.assertEquals(new_affiliate.type, 'affiliate')

    # Check that when changing the parent from an individual, it changes also
    # the address keeping the expected behaviour.
    def test_individual_changes_address_when_changing_parent_id(self):
        my_individual = self.partner_obj.create({
            'name': 'MyIndividual',
            'parent_id': self.first_company.id,
            'type': 'contact',
            'is_company': False,
            'street': 'individual street',
        })

        my_individual.parent_id = self.second_company.id
        my_individual.onchange_parent_id()

        # The parent have been changed.
        self.assertEquals(my_individual.parent_id.id, self.second_company.id)

        # The affiliate gets the address from the new parent.
        self.assertEquals(my_individual.street, "second company street",
                          "keeps the same street")
