# Copyright 2017-2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from psycopg2 import IntegrityError

from odoo import tools
from odoo.tests.common import TransactionCase


class TestResPartnerCompanyType(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_type = cls.env.ref(
            "partner_company_type.res_partner_company_type_sa"
        )

    def test_00_duplicate(self):
        # Test Duplicate Company type
        with self.assertRaises(IntegrityError), tools.mute_logger("odoo.sql_db"):
            self.company_type.create(dict(name=self.company_type.name))

    def test_create_company_type(self):
        # Test creating a new company type
        new_company_type = self.company_type.create(dict(name="New Company Type"))
        self.assertTrue(new_company_type, "New company type should be created")

    def test_update_company_type(self):
        # Test updating an existing company type
        self.company_type.write(dict(name="Updated Company Type"))
        self.assertEqual(
            self.company_type.name,
            "Updated Company Type",
            "Company type name should be updated",
        )

    def test_delete_company_type(self):
        # Test deleting a company type
        company_type_to_delete = self.company_type.create(
            dict(name="Company Type to Delete")
        )
        company_type_to_delete.unlink()
        self.assertFalse(
            company_type_to_delete.exists(), "Company type should be deleted"
        )
