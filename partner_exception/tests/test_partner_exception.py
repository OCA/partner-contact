# Copyright 2026 Foodles
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestPartnerException(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.rule = cls.env["exception.rule"].create(
            {
                "name": "Partner must have a ref",
                "sequence": 10,
                "model": "res.partner",
                "exception_type": "by_py_code",
                "code": "if not self.ref: failed=True",
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "Foo"})

    def test_reverse_field(self):
        self.assertEqual(self.env["res.partner"]._reverse_field(), "partner_ids")

    def test_fields_trigger_check_exception(self):
        self.assertEqual(
            self.env["res.partner"]._fields_trigger_check_exception(),
            ["ignore_exception"],
        )

    def test_detect_exception(self):
        self.partner.detect_exceptions()
        self.assertIn(self.rule, self.partner.exception_ids)
        self.assertTrue(self.partner.exceptions_summary)

    def test_no_exception_when_rule_passes(self):
        self.partner.ref = "OK"
        self.partner.detect_exceptions()
        self.assertFalse(self.partner.exception_ids)

    def test_write_ignore_exception_triggers_check(self):
        self.partner.detect_exceptions()
        self.assertTrue(self.partner.exception_ids)
        self.partner.write({"ignore_exception": True})
        # ignore_exception=True clears the linked exceptions
        self.assertTrue(self.partner.ignore_exception)
        self.assertFalse(self.partner.exception_ids)

    def test_write_without_trigger_field_skips_check(self):
        # Writing a non-trigger field on a partner with no prior detection
        # must not raise even though the partner would fail the rule.
        partner = self.env["res.partner"].create({"name": "Bar"})
        partner.write({"name": "Baz"})
        self.assertFalse(partner.exception_ids)

    def test_create_with_ignore_exception_triggers_check(self):
        partner = self.env["res.partner"].create(
            {"name": "Created", "ref": "X", "ignore_exception": True}
        )
        self.assertTrue(partner.ignore_exception)

    def test_create_with_ignore_exception_raises_on_failing_rule(self):
        # ignore_exception in vals triggers the check; a failing rule must raise.
        with self.assertRaises(ValidationError):
            self.env["res.partner"].create({"name": "Fails", "ignore_exception": False})

    def test_rule_partner_ids(self):
        self.rule.partner_ids = [(4, self.partner.id)]
        self.assertIn(self.partner, self.rule.partner_ids)
