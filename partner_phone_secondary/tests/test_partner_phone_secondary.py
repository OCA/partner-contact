# Copyright 2020 - Iván Todorovich
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

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

    def test_02_onchange_phone2_validation(self):
        is_phone_validation_functional = self.env["ir.module.module"].search(
            [("name", "=", "phone_validation"), ("state", "=", "installed")]
        )
        try:
            import phonenumbers  # noqa
        except ImportError:
            is_phone_validation_functional = False

        partner = self.env["res.partner"].create({"name": "Test Partner"})

        if not is_phone_validation_functional:
            # If phone_validation is not installed, the onchange should do nothing
            partner.phone2 = "1234567890"
            partner._onchange_phone2_validation()
            self.assertEqual(partner.phone2, "1234567890")
            return

        with patch(
            "odoo.addons.phone_validation.tools.phone_validation.phone_format"
        ) as mock_phone_format:
            mock_phone_format.return_value = "+1 234 567 890"
            partner.phone2 = "1234567890"
            # In real life, onchange is called by the client, so we call it manually
            partner._onchange_phone2_validation()
            mock_phone_format.assert_called()
            self.assertEqual(partner.phone2, "+1 234 567 890")

        # Test with empty phone2
        partner.phone2 = False
        partner._onchange_phone2_validation()
        self.assertFalse(partner.phone2)
