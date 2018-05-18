from odoo.tests import common


class TestPartnerAffiliate(common.TransactionCase):

    def setUp(self):
        super(TestPartnerAffiliate, self).setUp()
        self.partner_obj = self.env['res.partner']

        self.first_parent = self.partner_obj.create({
            'name': 'MyFirstParentForTheAffiliate',
            'type': 'contact',
            'is_company': True,
            'street': 'first parent street',
            'street2': 'number 99',
            'zip': 123,
            'city': 'Test City',
        })

        self.second_parent = self.partner_obj.create({
            'name': 'MySecondParentForTheAffiliate',
            'type': 'contact',
            'is_company': True,
            'street': 'second parent street',
            'street2': 'number 44',
            'zip': 999,
            'city': 'Test City',
        })

    # Check data integrity of the objects when an affiliate is given a new
    # parent. So both objects keeps their data.
    def test_change_parent_from_a_new_affiliate(self):
        new_affiliate = self.partner_obj.create({
            'name': 'MyTestAffiliate',
            'is_company': True,
            'parent_id': self.first_parent.id,
            'type': 'affiliate',
            'street': 'affiliate street',
            'street2': 'number 11',
            'zip': 567,
            'city': 'Test City',
            'email': 'myAffiliate@test.com',
        })

        # Checks for data integrity in affiliate and his parent.
        self.assertTrue(new_affiliate, "The new affiliate have been created.")

        self.assertEquals(new_affiliate.type, 'affiliate',
                          "Check type must be 'affiliate'")
        self.assertEquals(new_affiliate.parent_id.id, self.first_parent.id,
                          "Must be child of the parent defined in the setup")
        self.assertEquals(new_affiliate.street, "affiliate street",
                          "The street have been correctly set.")
        self.assertEquals(self.first_parent.street, "first parent street",
                          "The parent continues with his original street")

        # Change the parent of the affiliate for the second one in the set-up.
        new_affiliate.parent_id = self.second_parent.id
        new_affiliate.onchange_parent_id()

        # The parent have been changed. And is not the first one.
        self.assertEquals(new_affiliate.parent_id.id, self.second_parent.id)

        # The affiliate keeps its data for the street. Not modified.
        self.assertEquals(new_affiliate.street, "affiliate street",
                          "keeps the same street")
        # The data for the street of the first parent have not been changed.
        self.assertEquals(self.first_parent.street, "first parent street",
                          "keeps the same street")


    # Check that the default value for 'type' defined by default in the view
    # is set correctly when a new affiliate is created.
    def test_new_affiliate_is_created_with_type_affiliate_by_default(self):
        new_affiliate = self.partner_obj.with_context(
            {'default_parent_id': self.first_parent.id,
             'default_is_company': True,
             'default_type': 'affiliate'
             }
        ).create({
            'name': 'MyTestAffiliate',
            'street': 'affiliate street',
            'street2': 'number 11',
            'zip': 567,
            'city': 'Test City',
            'email': 'myAffiliate@test.com',
        })

        self.assertEquals(new_affiliate.type, 'affiliate')
