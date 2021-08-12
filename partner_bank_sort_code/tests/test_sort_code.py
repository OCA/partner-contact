# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from psycopg2 import IntegrityError

from odoo.tests import common
from odoo.tools import mute_logger


class TestSortCode(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create two different active bank with different sort codes
        cls.Bank = cls.env["res.bank"]
        vals = {
            "name": "BANK 1",
            "sort_code": "95-01-32",
        }
        cls.bank_1 = cls.Bank.create(vals)
        vals = {
            "name": "BANK 2",
            "sort_code": "95-01-33",
        }
        cls.bank_2 = cls.Bank.create(vals)

    def test_sort_code_duplicate(self):
        # Create a duplicate
        vals = {
            "name": "BANK 3",
            "sort_code": "95-01-32",
        }
        with self.assertRaises(IntegrityError), mute_logger("odoo.sql_db"):
            self.Bank.create(vals)

    def test_sort_code(self):
        # Create a new bank with new sort code
        vals = {
            "name": "BANK 3",
            "sort_code": "95-01-34",
        }
        self.Bank.create(vals)

    def test_sort_code_inactive(self):
        # Set several banks with same sort code to inactive and then create
        # a bank with that sort code
        self.bank_1.write({"active": False})
        vals = {
            "name": "BANK 3",
            "sort_code": "95-01-38",
        }
        self.bank_3 = self.Bank.create(vals)
        self.bank_3.active = False
        self.bank_3.flush()
        vals = {
            "name": "BANK 4",
            "sort_code": "95-01-38",
        }
        self.Bank.create(vals)
