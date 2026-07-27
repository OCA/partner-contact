# Copyright 2017-2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from psycopg2 import IntegrityError

from odoo import tools

from odoo.addons.base.tests.common import BaseCommon


class TestResPartnerCompanyType(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_type = cls.env["res.partner.company.type"].create(
            {
                "name": "Test Anonymous Company",
                "shortcut": "AC",
            }
        )

    def test_00_duplicate(self):
        # Test Duplicate Company type

        with self.assertRaises(IntegrityError), tools.mute_logger("odoo.sql_db"):
            self.company_type.create(dict(name=self.company_type.name))
