# Copyright (C) 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests import common


class TestResPartner(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.dea_category_id = cls.env.ref(
            "partner_identification_dea.res_partner_id_category_dea",
            raise_if_not_found=False,
        )
        cls.medical_id = cls.env.ref(
            "partner_identification_dea.res_partner_id_category_medical",
            raise_if_not_found=False,
        )
        cls.controlled_id = cls.env.ref(
            "partner_identification_dea.res_partner_id_category_controlled_substance",
            raise_if_not_found=False,
        )
        cls.date = fields.Date.today() + relativedelta(days=30)
        cls.expired_date = fields.Date.today() - relativedelta(days=10)
        cls.partner_obj = cls.env["res.partner"]
        cls.partner_number_obj = cls.env["res.partner.id_number"]
        cls.partner_roy = cls.partner_obj.create({"name": "Roy"})
        cls.partner_jimmy = cls.partner_obj.create({"name": "Jimmy"})
        cls.partner_john = cls.partner_obj.create({"name": "John"})
        cls.partner_number_obj.create(
            {
                "partner_id": cls.partner_roy.id,
                "category_id": cls.dea_category_id.id,
                "status": "open",
                "valid_until": cls.date,
                "name": "AA1270533",
            }
        )
        cls.partner_number_obj.create(
            {
                "partner_id": cls.partner_jimmy.id,
                "category_id": cls.medical_id.id,
                "status": "open",
                "valid_until": cls.date,
                "name": "12360001",
            }
        )
        cls.controlled_number = cls.partner_number_obj.create(
            {
                "partner_id": cls.partner_john.id,
                "category_id": cls.controlled_id.id,
                "status": "open",
                "valid_until": cls.date,
                "name": "78901234",
            }
        )

    def test_dea_and_medical_license_fields_computed(self):
        """Test DEA and medical license fields computed from ID numbers."""
        self.partner_roy.invalidate_recordset()
        self.partner_jimmy.invalidate_recordset()
        self.assertEqual(self.partner_roy.dea_number, "AA1270533")
        self.assertEqual(self.partner_roy.dea_expired_date, self.date)
        self.assertEqual(self.partner_jimmy.medical_license, "12360001")
        self.assertEqual(self.partner_jimmy.medical_license_expired_date, self.date)

    def test_contr_subst_license_fields_computed(self):
        """Test controlled substance license fields computed from ID number."""
        self.partner_john.invalidate_recordset()
        self.assertEqual(self.partner_john.contr_subst_license, "78901234")
        self.assertEqual(self.partner_john.contr_subst_expired_date, self.date)

    def test_contr_subst_license_expired_or_inactive(self):
        """Test license is ignored if expired or inactive."""
        self.controlled_number.status = "close"
        self.partner_john.invalidate_recordset()
        self.assertEqual(self.partner_john.contr_subst_license, "")
        self.assertFalse(self.partner_john.contr_subst_expired_date)
        self.controlled_number.write(
            {
                "status": "open",
                "valid_until": self.expired_date,
            }
        )
        self.partner_john.invalidate_recordset()
        self.assertEqual(self.partner_john.contr_subst_license, "78901234")
        self.assertEqual(self.partner_john.contr_subst_expired_date, self.expired_date)

    def test_name_search_by_contr_subst_license(self):
        """Test name_search can find partner by controlled substance license."""
        result = self.partner_obj.name_search(name="78901234")
        self.assertTrue(result)
        self.assertEqual(result[0][0], self.partner_john.id)
        self.assertIn("John", result[0][1])

    def test_send_expiration_date_notification(self):
        self.partner_obj.send_expiration_date_notification()
