# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestEORI(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        country_uk = cls.env.ref("base.uk")
        state_uk = cls.env["res.country.state"].search(
            [("country_id", "=", country_uk.id)], limit=1
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "TestEORI",
                "country_id": country_uk.id,
                "state_id": state_uk.id,
            }
        )
        cls.partner2 = cls.env["res.partner"].create(
            {
                "name": "TestEORI2",
                "country_id": country_uk.id,
                "state_id": state_uk.id,
            }
        )
        pc = cls.env.ref(
            "partner_identification_eori.partner_identification_eori_number_category"
        )
        cls.partner_id_category = pc

    def test_eori(self):
        # Good EORI
        vals = {"name": "GB941785887000", "category_id": self.partner_id_category.id}

        self.partner.write({"id_numbers": [Command.create(vals)]})
        id_number = self.partner.id_numbers[0]

        self.assertEqual(id_number.name, "GB941785887000")

        # Duplicate EORI
        vals = {"name": "GB941785887000", "category_id": self.partner_id_category.id}

        with self.assertRaises(ValidationError):
            self.partner2.write({"id_numbers": [Command.create(vals)]})

        # Wrong EORI
        vals = {"name": "941785887000", "category_id": self.partner_id_category.id}
        with self.assertRaises(ValidationError):
            self.partner.write({"id_numbers": [Command.create(vals)]})

    def test_eori_with_no_number(self):
        self.assertFalse(
            self.partner_id_category.validate_res_partner_eori(id_number=None)
        )
