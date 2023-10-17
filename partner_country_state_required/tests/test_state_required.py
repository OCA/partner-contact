# Copyright 2023 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestCountryStateRequired(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestCountryStateRequired, cls).setUpClass()
        cls.partner_model = cls.env["res.partner"]
        cls.spain = cls.env.ref("base.es")
        cls.state_bcn = cls.env.ref("base.state_es_b")

    def test_create_partner(self):
        self.spain.state_required = True
        vals = {
            "name": "Test Partner 1",
            "country_id": self.spain.id,
        }
        with self.assertRaisesRegex(
            ValidationError,
            "Please specify a state for the address when selecting "
            "a country with available states.",
        ):
            self.partner_model.create(vals)

        vals["state_id"] = self.state_bcn.id
        partner = self.partner_model.create(vals)

        self.assertTrue(partner)

    def test_write_partner(self):
        self.spain.state_required = True
        vals = {
            "name": "Test Partner 2",
        }
        partner = self.partner_model.create(vals)

        with self.assertRaisesRegex(
            ValidationError,
            "Please specify a state for the address when selecting "
            "a country with available states.",
        ):
            partner.write(
                {
                    "country_id": self.spain.id,
                }
            )

        write_vals = {
            "country_id": self.spain.id,
            "state_id": self.state_bcn.id,
        }

        partner.write(write_vals)

        self.assertEqual(partner.state_id.code, "B")

    def test_create_partner_with_context(self):
        vals = {
            "name": "Test Partner 3",
            "country_id": self.spain.id,
        }
        partner = self.partner_model.with_context(no_state_required=True).create(vals)

        self.assertTrue(partner)

    def test_create_partner_country_state_required(self):
        self.spain.state_required = False

        vals = {
            "name": "Test Partner 2",
            "country_id": self.spain.id,
        }
        partner = self.partner_model.create(vals)

        self.assertTrue(partner)
