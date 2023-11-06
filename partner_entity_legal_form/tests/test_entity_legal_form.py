# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo.exceptions import UserError
from odoo.tests import common


class TestPartnerEntityLegalForm(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestPartnerEntityLegalForm, cls).setUpClass()

        cls.partner_entity_legal_form_model = cls.env["entity.legal.form"]

        cls.country_es = cls.env.ref("base.es")
        cls.country_us = cls.env.ref("base.us")
        cls.state_california = cls.env.ref("base.state_us_5")

        cls.partner_id = cls.env.ref("base.res_partner_2")

    def test_01_partner_entity_legal_form_country(self):
        """Test to set up an entity_legal_form_id according to the country of the partner_id,
        check that raises an error if they don't match."""
        us_entity_legal_form = self.partner_entity_legal_form_model.search(
            [("country_id", "=", self.country_us.id)], limit=1
        )
        es_entity_legal_form = self.partner_entity_legal_form_model.search(
            [("country_id", "=", self.country_es.id)], limit=1
        )

        self.partner_id.write(
            {
                "country_id": self.country_us.id,
                "entity_legal_form_id": us_entity_legal_form.id,
            }
        )
        self.assertEqual(self.partner_id.entity_legal_form_id, us_entity_legal_form)

        with self.assertRaises(UserError):
            self.partner_id.write(
                {
                    "entity_legal_form_id": es_entity_legal_form.id,
                }
            )

    def test_02_partner_entity_legal_form_state(self):
        """Test to set up an entity_legal_form_id according to the state of the partner_id,
        check that raises an error if they don't match."""
        us_ca_entity_legal_form = self.partner_entity_legal_form_model.search(
            [
                ("country_id", "=", self.country_us.id),
                ("state_id", "=", self.state_california.id),
            ],
            limit=1,
        )
        us_no_ca_entity_legal_form = self.partner_entity_legal_form_model.search(
            [
                ("country_id", "=", self.country_us.id),
                ("state_id", "!=", False),
                ("state_id", "!=", self.state_california.id),
            ],
            limit=1,
        )

        self.partner_id.write(
            {
                "country_id": self.country_us.id,
                "state_id": self.state_california.id,
                "entity_legal_form_id": us_ca_entity_legal_form.id,
            }
        )
        self.assertEqual(self.partner_id.entity_legal_form_id, us_ca_entity_legal_form)

        with self.assertRaises(UserError):
            self.partner_id.write(
                {
                    "entity_legal_form_id": us_no_ca_entity_legal_form.id,
                }
            )

    def test_03_partner_entity_legal_form_abbreviation_id(self):
        """Test to set up an entity_legal_form_abbreviation_id according to the
        entity_legal_form_id of the partner_id, check that raises an error if
        they don't match."""
        us_ca_entity_legal_form = self.partner_entity_legal_form_model.search(
            [
                ("country_id", "=", self.country_us.id),
                ("state_id", "=", self.state_california.id),
                ("abbreviation_ids", "!=", False),
            ],
            limit=1,
        )

        self.partner_id.write(
            {
                "country_id": self.country_us.id,
                "state_id": self.state_california.id,
                "entity_legal_form_id": us_ca_entity_legal_form.id,
                "entity_legal_form_abbreviation_id": us_ca_entity_legal_form.abbreviation_ids[
                    0
                ].id,
            }
        )

        other_us_ca_entity_legal_form = self.partner_entity_legal_form_model.search(
            [
                ("id", "!=", us_ca_entity_legal_form.id),
                ("country_id", "=", self.country_us.id),
                ("state_id", "=", self.state_california.id),
            ],
            limit=1,
        )
        with self.assertRaises(UserError):
            self.partner_id.write(
                {
                    "entity_legal_form_id": other_us_ca_entity_legal_form.id,
                }
            )
