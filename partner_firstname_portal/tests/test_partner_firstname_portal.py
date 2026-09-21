# Copyright 2025 Sylvain LE GAL (GRAP)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import http
from odoo.fields import Command
from odoo.tests.common import HttpCase


class TestPartnerFirstnamePortal(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Generated with https://www.fakenamegenerator.com
        cls.partner_portal = cls.env["res.partner"].create(
            {
                "name": "Théodule Bernier",
                "email": "theodule_bernier@jourrapide.com",
                "country_id": cls.env.ref("base.be").id,
                "phone": "0487 49 15 23",
                "street": "Hooivelden 198",
                "zip": "4720",
                "city": "La calamine",
            }
        )
        cls.user_portal = cls.env["res.users"].create(
            {
                "login": "portal",
                "password": "portal",
                "partner_id": cls.partner_portal.id,
                "group_ids": [Command.set([cls.env.ref("base.group_portal").id])],
            }
        )
        cls.base_data = {
            "name": cls.user_portal.partner_id.name,
            "partner_id": cls.user_portal.partner_id.id,
            "country_id": cls.user_portal.country_id.id,
            "email": cls.user_portal.email,
            "phone": cls.user_portal.phone,
            "street": cls.user_portal.street,
            "city": cls.user_portal.city,
            "zip": cls.user_portal.zip,
        }

    def _set_required_field(self, value):
        self.env["ir.config_parameter"].set_param(
            "partner_firstname.required_fields", value
        )

    def _post_account_details(self, **data):
        self.authenticate(self.user_portal.login, "admin")
        data["csrf_token"] = http.Request.csrf_token(self)
        return self.url_open("/my/address/submit", data=data)

    def test_edition_individual_missing_firstname(self):
        self._set_required_field("firstname")
        self._post_account_details(
            **self.base_data,
            lastname="MY LAST NAME portal",
        )
        self.assertEqual(
            self.user_portal.name,
            "Théodule Bernier",
            "Should not change name, if required firstname is missing",
        )

    def test_edition_individual_missing_lastname(self):
        self._set_required_field("lastname")
        self._post_account_details(
            **self.base_data,
            firstname="My First Name portal",
        )
        self.assertEqual(
            self.user_portal.partner_id.name,
            "Théodule Bernier",
            "Should not change name, if required lastname is missing",
        )

    def test_edition_individual_missing_lastname_and_firstname(self):
        self._set_required_field("no")
        self._post_account_details(
            **self.base_data,
        )
        self.assertEqual(
            self.user_portal.partner_id.name,
            "Théodule Bernier",
            "Should not change name, if lastname and firstname is missing",
        )

    def test_edition_individual_with_new_firstname_and_lastname(self):
        self._post_account_details(
            **self.base_data,
            firstname="My First Name portal",
            lastname="MY LAST NAME portal",
        )
        self.assertEqual(
            self.user_portal.partner_id.name, "My First Name portal MY LAST NAME portal"
        )

    def test_edition_company_missing_new_name(self):
        self.user_portal.partner_id.company_type = "company"
        self._post_account_details(**self.base_data)
        self.assertEqual(self.user_portal.partner_id.name, "Théodule Bernier")

    def test_edition_company_with_new_name(self):
        self.user_portal.partner_id.is_company = True
        self.base_data["name"] = "My New Company Name"
        self._post_account_details(**self.base_data)
        self.assertEqual(self.user_portal.partner_id.name, "My New Company Name")
