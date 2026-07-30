# Copyright 2025 Sylvain LE GAL (GRAP)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import http

from odoo.addons.auth_signup.tests.test_auth_signup import TestAuthSignupFlow


class TestPartnerFirstnameAuthSignup(TestAuthSignupFlow):
    def test_signup_workflow_correct_names_fields(self):
        # Activate free signup
        self._activate_free_signup()

        # Get csrf_token
        self.authenticate(None, None)
        csrf_token = http.Request.csrf_token(self)

        # 1. Check if user name is correctly computed
        payload = {
            "login": "partner_firstname_auth_signup@example.com",
            "firstname": "My First Name auth_signup",
            "lastname": "MY LAST NAME auth_signup",
            "password": "mypassword",
            "confirm_password": "mypassword",
            "csrf_token": csrf_token,
        }
        url_free_signup = self._get_free_signup_url()
        self.url_open(url_free_signup, data=payload)
        new_user = self.env["res.users"].search(
            [("login", "=", "partner_firstname_auth_signup@example.com")]
        )
        self.assertTrue(new_user)

        self.assertEqual(
            new_user.name, "My First Name auth_signup MY LAST NAME auth_signup"
        )

    def test_signup_workflow_incorrect_names_fields(self):
        # Activate free signup
        self._activate_free_signup()

        # Get csrf_token
        self.authenticate(None, None)
        csrf_token = http.Request.csrf_token(self)

        payload = {
            "login": "partner_firstname_auth_signup@example.com",
            "password": "mypassword",
            "confirm_password": "mypassword",
            "csrf_token": csrf_token,
        }
        url_free_signup = self._get_free_signup_url()
        self.url_open(url_free_signup, data=payload)
        new_user = self.env["res.users"].search(
            [("login", "=", "partner_firstname_auth_signup@example.com")]
        )
        self.assertFalse(new_user)
