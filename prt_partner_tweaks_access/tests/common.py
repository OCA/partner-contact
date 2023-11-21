from odoo.tests.common import TransactionCase


class PartnerTweaksAccessCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        cls.partner_model = cls.env["res.partner"]
        cls.user_model = cls.env["res.users"]
        cls.partner_category = cls.env["res.partner.category"]

        cls.test_category1 = cls.partner_category.create({"name": "Test category 1"})
        cls.test_category2 = cls.partner_category.create({"name": "Test category 2"})
        cls.user_with_tweaks_access = cls.user_model.with_context(
            no_reset_password=True
        ).create(
            {
                "name": "Test User with Tweaks Access",
                "login": "user_with_tweaks_access@test.com",
            }
        )
        cls.user_with_tweaks_access.groups_id = [
            (4, cls.env.ref("prt_partner_tweaks_access.prt_contact_users").id)
        ]
        cls.country = cls.env.ref("base.au")
        cls.country_state = cls.env.ref("base.state_au_7")

        cls.partner1 = cls.partner_model.create(
            {
                "name": "Test1",
                "email": "test1@test.com",
                "country_id": cls.country.id,
                "state_id": cls.country_state.id,
                "category_id": cls.test_category1,
            }
        )

        cls.partner2 = cls.partner_model.create(
            {
                "name": "Test2",
                "email": "test2@test.com",
                "category_id": cls.test_category2,
            }
        )
