# Copyright 2020 - Iván Todorovich
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, tagged


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

        # No Form(): it needs module 'web', which is not a dependency
        partner = self.env["res.partner"].create(
            {
                "name": "Test Partner",
                "country_id": self.env.ref("base.be").id,
                "phone": "0456998877",
                "phone2": "0456998899",
            }
        )

        # Odoo 20: raw input is kept, formatted value lives in companion fields
        self.assertEqual(partner.phone, "0456998877")
        self.assertEqual(partner.phone2, "0456998899")
        if is_phone_validation_functional:
            self.assertEqual(partner.phone_formatted, "+32 456 99 88 77")
            self.assertEqual(partner.phone2_formatted, "+32 456 99 88 99")
            self.assertEqual(partner.phone2_sanitized, "+32456998899")
        else:
            self.assertFalse(partner.phone2_formatted)

    def test_02_phone2_companion_fields(self):
        is_phone_validation_functional = self.env["ir.module.module"].search(
            [("name", "=", "phone_validation"), ("state", "=", "installed")]
        )
        try:
            import phonenumbers  # noqa
        except ImportError:
            is_phone_validation_functional = False

        partner = self.env["res.partner"].create(
            {"name": "Test Partner", "country_id": self.env.ref("base.th").id}
        )
        partner.phone2 = "0 92 297 7777"
        self.assertEqual(partner.phone2, "0 92 297 7777")
        if is_phone_validation_functional:
            self.assertEqual(partner.phone2_sanitized, "+66922977777")
            self.assertEqual(partner.phone2_formatted, "+66 92 297 7777")
        else:
            self.assertFalse(partner.phone2_formatted)

        partner.phone2 = False
        self.assertFalse(partner.phone2_sanitized)
        self.assertFalse(partner.phone2_formatted)
