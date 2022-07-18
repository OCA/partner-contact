# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from psycopg2 import IntegrityError

from odoo.tests.common import SavepointCase
from odoo.tools.misc import mute_logger


class TestPartnerUom(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "A good partner",
            }
        )

        cls.partner_uom = cls.env["partner.uom"].create(
            {
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "partner_id": cls.partner.id,
                "partner_uom": "Uni",
            }
        )

    def test_partner_uom(self):
        self.assertEqual(
            self.partner_uom.display_name, str("A good partner (Uni > Units)")
        )

    @mute_logger("odoo.sql_db")
    def test_partner_duplicate_uom(self):
        with self.assertRaises(IntegrityError):
            self.env["partner.uom"].create(
                {
                    "uom_id": self.env.ref("uom.product_uom_unit").id,
                    "partner_id": self.partner.id,
                    "partner_uom": "Uni",
                }
            )

    @mute_logger("odoo.sql_db")
    def test_partner_duplicate(self):
        self.partner_uom.active = False
        self.partner_uom.flush()
        self.env["partner.uom"].create(
            {
                "uom_id": self.env.ref("uom.product_uom_unit").id,
                "partner_id": self.partner.id,
                "partner_uom": "Uni",
            }
        )
