# Copyright 2025 Sylvain LE GAL (GRAP)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import http
from odoo.tests.common import HttpCase


class TestPartnerFirstnamePortal(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env.ref("base.user_admin")

    def _authenticate_and_get_payload(self):
        # Get csrf_token
        self.authenticate(self.user.login, "admin")
        payload = {
            "name": "Mitchell Admin",
            "country_id": self.user.country_id.id,
            "email": self.user.email,
            "phone": self.user.phone,
            "street": self.user.street,
            "city": self.user.city,
            "csrf_token": http.Request.csrf_token(self),
        }
        return payload

    def test_editition_without_new_names(self):
        payload = self._authenticate_and_get_payload()
        self.url_open("/my/account", data=payload)
        self.assertEqual(self.user.name, "Mitchell Admin")

    def test_edition_with_new_names(self):
        payload = self._authenticate_and_get_payload()
        payload.update(
            {
                "firstname": "My First Name portal",
                "lastname": "MY LAST NAME portal",
            }
        )
        self.url_open("/my/account", data=payload)

        self.assertEqual(self.user.name, "My First Name portal MY LAST NAME portal")
