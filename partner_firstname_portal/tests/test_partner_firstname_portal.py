# Copyright 2025 Sylvain LE GAL (GRAP)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import http
from odoo.tests.common import HttpCase


class TestPartnerFirstnamePortal(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env.ref("base.user_admin")
        cls.base_data = {
            "name": "Mitchell Admin",
            "country_id": cls.user.country_id.id,
            "email": cls.user.email,
            "phone": cls.user.phone,
            "street": cls.user.street,
            "city": cls.user.city,
        }

    def _set_required_field(self, value):
        self.env["ir.config_parameter"].set_param(
            "partner_firstname.required_fields", value
        )

    def _post_account_details(self, **data):
        self.authenticate(self.user.login, "admin")
        data["csrf_token"] = http.Request.csrf_token(self)
        return self.url_open("/my/account", data=data)

    def test_edition_individual_missing_firstname(self):
        self._set_required_field("firstname")
        self._post_account_details(
            **self.base_data,
            lastname="MY LAST NAME portal",
        )
        self.assertEqual(
            self.user.name,
            "Mitchell Admin",
            "Should not change name, if required firstname is missing",
        )

    def test_edition_individual_missing_lastname(self):
        self._set_required_field("lastname")
        self._post_account_details(
            **self.base_data,
            firstname="My First Name portal",
        )
        self.assertEqual(
            self.user.name,
            "Mitchell Admin",
            "Should not change name, if required lastname is missing",
        )

    def test_edition_individual_missing_lastname_and_firstname(self):
        self._set_required_field("no")
        self._post_account_details(
            **self.base_data,
        )
        self.assertEqual(
            self.user.name,
            "Mitchell Admin",
            "Should not change name, if lastname and firstname is missing",
        )

    def test_edition_individual_with_new_firstname_and_lastname(self):
        self._post_account_details(
            **self.base_data,
            firstname="My First Name portal",
            lastname="MY LAST NAME portal",
        )
        self.assertEqual(self.user.name, "My First Name portal MY LAST NAME portal")

    def test_edition_company_missing_new_name(self):
        self.user.partner_id.company_type = "company"
        self._post_account_details(**self.base_data)
        self.assertEqual(self.user.name, "Mitchell Admin")

    def test_edition_company_with_new_name(self):
        self.user.partner_id.is_company = True
        self.base_data["name"] = "My New Company Name"
        self._post_account_details(**self.base_data)
        self.assertEqual(self.user.name, "My New Company Name")
