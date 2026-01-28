# Copyright 2016-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from unittest.mock import patch

from odoo.tests.common import TransactionCase


class TestPartnerContactGender(TransactionCase):
    def setUp(self):
        super().setUp()
        self.testpartner_none = self.env["res.partner"].create(
            {
                "name": "test",
            }
        )
        self.testpartner_male = self.env["res.partner"].create(
            {
                "name": "test",
                "gender": "male",
            }
        )
        self.testpartner_female = self.env["res.partner"].create(
            {
                "name": "test",
                "gender": "female",
            }
        )

    def test_partner_contact_gender(self):
        self.assertFalse(self.testpartner_none.gender)
        self.assertEqual(self.testpartner_male.gender, "male")
        self.assertEqual(self.testpartner_female.gender, "female")

    def test_partner_contact_gender_title(self):
        from .. import hooks

        if not hooks.has_module_partner_title(self.env):
            self.skipTest("partner_title module not installed")

        testpartner_title_madam = self.env["res.partner"].create(
            {
                "name": "test",
                "title_id": self.env.ref("partner_title.res_partner_title_madam").id,
            }
        )
        hooks.post_init_hook(self.env)
        self.assertEqual(testpartner_title_madam.gender, "female")
        self.assertFalse(self.testpartner_none.gender)

    def test_partner_contact_gender_no_title_module(self):
        testpartner = self.env["res.partner"].create(
            {
                "name": "test",
            }
        )

        from .. import hooks

        with patch(
            "odoo.addons.partner_contact_gender.hooks.has_module_partner_title",
            return_value=False,
        ):
            hooks.post_init_hook(self.env)

        self.assertFalse(testpartner.gender)
