# Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import Form, SavepointCase


class TestPartnerDuns(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.partner = cls.env.ref("base.res_partner_1")
        cls.partner.duns = "123456789"

    def test_partner_duns_sanitized_on_create(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Test",
                "duns": "111-222-333",
            }
        )
        self.assertEqual(partner.duns, "111222333")

    def test_partner_duns_sanitized_on_write(self):
        self.partner.duns = "111-222-333"
        self.assertEqual(self.partner.duns, "111222333")

    def test_partner_duns_sanitized_on_change(self):
        with Form(self.partner) as form:
            form.duns = "111-222-333"
            self.assertEqual(form.duns, "111222333")

    def test_partner_duns_duplicated(self):
        dupe = self.env["res.partner"].create(
            {
                "name": "Duplicated",
                "duns": "123456789",
            }
        )
        self.assertEqual(dupe.same_duns_partner_id, self.partner)
        dupe.duns = "000000000"
        self.assertFalse(dupe.same_duns_partner_id)
