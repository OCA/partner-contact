# Copyright 2020 - Iván Todorovich
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import Form, TransactionCase


class TestPartnerPhoneSecondary(TransactionCase):
    def test_01_phone_validation_compatibility(self):
        # This is here only to get code coverage.
        with Form(self.env["res.partner"]) as form:
            form.name = "French Partner"
            form.country_id = self.env.ref("base.fr")
            form.phone = "766666666"
            form.phone2 = "766666666"
            # It's not the purpose of this module to test phone_validation,
            # nor how it formats phone numbers. Also it's not directly depended
            # by this module. We do know for sure, though, that the same number
            # is going to be formatted in the exact same way.
            self.assertEqual(form.phone, form.phone2)
