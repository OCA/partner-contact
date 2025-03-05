# Copyright 2020 - Iván Todorovich
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import Form, TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPartnerPhoneSecondary(TransactionCase):
    def test_01_phone_validation_compatibility(self):
        is_phone_validation_functional = self.env["ir.module.module"].search(
            [("name", "=", "phone_validation"), ("state", "=", "installed")]
        )
        try:
            import phonenumbers  # noqa
        except ImportError:
            is_phone_validation_functional = False

        form = Form(self.env["res.partner"])
        form.country_id = self.env.ref("base.be")
        form.phone = "0456998877"
        form.phone2 = "0456998899"

        if is_phone_validation_functional:
            self.assertEqual(form.phone, "+32 456 99 88 77")
            self.assertEqual(form.phone2, "+32 456 99 88 99")
        else:
            self.assertEqual(form.phone, "0456998877")
            self.assertEqual(form.phone2, "0456998899")
