# Copyright 2025 Sylvain LE GAL (GRAP)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


import odoo.tests
from odoo import http

from odoo.addons.auth_signup.tests.test_auth_signup import TestAuthSignupFlow


@odoo.tests.tagged("post_install", "-at_install")
class TestPartnerIscompanyAuthSignup(TestAuthSignupFlow):
    def test_signup_workflow_company(self):
        # Activate free signup
        self._activate_free_signup()

        # Get csrf_token
        self.authenticate(None, None)
        csrf_token = http.Request.csrf_token(self)

        # 1. Check if user name is correctly computed
        payload = {
            "login": "partner_is_company_auth_signup@example.com",
            "name": "New Company",
            "company_type": "company",
            "password": "mypassword",
            "confirm_password": "mypassword",
            "csrf_token": csrf_token,
        }
        url_free_signup = self._get_free_signup_url()
        self.url_open(url_free_signup, data=payload)
        new_user = self.env["res.users"].search(
            [("login", "=", "partner_is_company_auth_signup@example.com")]
        )
        self.assertTrue(new_user)
        self.assertTrue(new_user.is_company)

    def test_signup_workflow_person(self):
        # Activate free signup
        self._activate_free_signup()

        # Get csrf_token
        self.authenticate(None, None)
        csrf_token = http.Request.csrf_token(self)

        payload = {
            "login": "partner_is_company_auth_signup@example.com",
            "name": "New Individual",
            "company_type": "person",
            "password": "mypassword",
            "confirm_password": "mypassword",
            "csrf_token": csrf_token,
        }
        url_free_signup = self._get_free_signup_url()
        self.url_open(url_free_signup, data=payload)
        new_user = self.env["res.users"].search(
            [("login", "=", "partner_is_company_auth_signup@example.com")]
        )
        self.assertTrue(new_user)
        self.assertFalse(new_user.is_company)

    def test_signup_retrieve_info(self):
        partner_dummy = self.env["res.partner"].create(
            {
                "name": "Dummy Partner",
            }
        )
        partner_dummy.signup_prepare()
        token_invalid = partner_dummy._generate_signup_token()
        partner_dummy.signup_cancel()
        res_invalid = self.env["res.partner"]._signup_retrieve_info(token_invalid)
        self.assertFalse(res_invalid)

        partner_company = self.env["res.partner"].create(
            {
                "name": "Test Company Partner",
                "is_company": True,
            }
        )
        partner_company.signup_prepare()
        token_company = partner_company._generate_signup_token()
        res_company = self.env["res.partner"]._signup_retrieve_info(token_company)
        self.assertEqual(res_company.get("company_type"), "company")

        partner_person = self.env["res.partner"].create(
            {
                "name": "Test Person Partner",
                "is_company": False,
            }
        )
        partner_person.signup_prepare()
        token_person = partner_person._generate_signup_token()
        res_person = self.env["res.partner"]._signup_retrieve_info(token_person)
        self.assertEqual(res_person.get("company_type"), "person")
