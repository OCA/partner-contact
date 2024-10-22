# Copyright 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase

from .. import post_init_hook


class TestPartnerStage(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Stage = cls.env["res.partner.stage"]
        cls.Partner = cls.env["res.partner"]

        # Create some test partners without a stage
        cls.partner_1 = cls.env["res.partner"].create(
            {
                "name": "Partner 1",
                "stage_id": False,
            }
        )
        cls.partner_2 = cls.env["res.partner"].create(
            {
                "name": "Partner 2",
                "stage_id": False,
            }
        )

    def test_01_post_init_hook(self):
        """Test post_init_hook sets the default stage on partners without stage_id"""

        # Ensure partners initially have no stage
        self.assertFalse(self.partner_1.stage_id)
        self.assertFalse(self.partner_2.stage_id)

        post_init_hook(self.env)

        # Reload the partners from the database to get the updated values
        self.partner_1.invalidate_recordset()
        self.partner_2.invalidate_recordset()

        # Check if partners' stages have been updated
        self.assertEqual(
            self.partner_1.stage_id, self.env.ref("partner_stage.partner_stage_active")
        )
        self.assertEqual(
            self.partner_2.stage_id, self.env.ref("partner_stage.partner_stage_active")
        )
        self.assertEqual(self.partner_1.stage_id.state, "confirmed")
        self.assertEqual(self.partner_2.stage_id.state, "confirmed")

        post_init_hook(self.env)

        # Reload the partners from the database to get the updated values
        self.partner_1.invalidate_recordset()
        self.partner_2.invalidate_recordset()

        # Check if partners' stages have been updated
        self.assertEqual(
            self.partner_1.stage_id, self.env.ref("partner_stage.partner_stage_active")
        )
        self.assertEqual(
            self.partner_2.stage_id, self.env.ref("partner_stage.partner_stage_active")
        )
        self.assertEqual(self.partner_1.stage_id.state, "confirmed")
        self.assertEqual(self.partner_2.stage_id.state, "confirmed")

    def test_02_partner_stage(self):
        default_stage = self.env.ref("partner_stage.partner_stage_active")
        new_partner = self.Partner.create({"name": "A Partner"})
        self.assertTrue(new_partner.stage_id, default_stage)
        states = new_partner._read_group_stage_id(self.Stage, [], None)
        self.assertTrue(states.ids, [1, 2, 3])

    def test_03_stage_default_constraint(self):
        with self.assertRaises(ValidationError):
            self.Stage.create({"name": "Another Default Stage", "is_default": True})
