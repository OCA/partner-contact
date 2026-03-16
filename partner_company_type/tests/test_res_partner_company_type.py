# Copyright 2017-2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

try:
    from psycopg import errors as psycopg_errors
except ImportError:
    from psycopg2 import errors as psycopg_errors

from odoo import tools
from odoo.tests.common import TransactionCase


class TestResPartnerCompanyType(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_type = cls.env["res.partner.company.type"].create(
            {"name": "SA Test", "shortcut": "SAT"}
        )

    def test_00_duplicate(self):
        # Test Duplicate Company type

        with (
            self.assertRaises(psycopg_errors.UniqueViolation),
            tools.mute_logger("odoo.sql_db"),
        ):
            self.env["res.partner.company.type"].create(
                {"name": self.company_type.name}
            )
