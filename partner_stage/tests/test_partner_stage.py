# Copyright 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestPartnerStage(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Stage = cls.env["res.partner.stage"]
        cls.Partner = cls.env["res.partner"]

    def test_01_partner_stage(self):
        default_stage = self.env.ref("partner_stage.partner_stage_active")
        new_partner = self.Partner.create({"name": "A Partner"})
        self.assertTrue(new_partner.stage_id, default_stage)

    def test_02_stage_default_constraint(self):
        with self.assertRaises(ValidationError) as ctx:
            self.Stage.create({"name": "Another Default Stage", "is_default": True})
            err_msg = ctx.exception.args[0]
            self.assertEqual("There should be only one default stage", err_msg)
