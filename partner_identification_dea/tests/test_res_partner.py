# Copyright (C) 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.exceptions import ValidationError
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
        self.partner_roy.email = "roy@example.com"
        self.partner_obj.send_expiration_date_notification()

    def test_send_expiration_date_notification_without_template(self):
        self.env.ref(
            "partner_identification_dea.email_template_dea_notification"
        ).unlink()
        self.partner_obj.send_expiration_date_notification()

    def test_get_open_id_number_without_category(self):
        self.assertFalse(self.partner_roy._get_open_id_number(False))

    def test_name_search_empty_value(self):
        result = self.partner_obj.name_search(name="")
        self.assertTrue(result)

    def test_search_display_name_without_like_operator(self):
        domain = self.partner_obj._search_display_name("!=", "John")
        self.assertTrue(domain)

    def test_dea_checksum_validation(self):
        with self.assertRaises(ValidationError):
            self.partner_number_obj.create(
                {
                    "partner_id": self.partner_roy.id,
                    "category_id": self.dea_category_id.id,
                    "status": "draft",
                    "name": "AA1270539",
                }
            )

    def test_create_open_id_closes_previous(self):
        first = self.partner_roy.id_numbers.filtered(
            lambda number: number.category_id == self.dea_category_id
        )
        self.assertEqual(first.status, "open")
        second = self.partner_number_obj.create(
            {
                "partner_id": self.partner_roy.id,
                "category_id": self.dea_category_id.id,
                "status": "open",
                "valid_until": self.date,
                "name": "AB1234563",
            }
        )
        self.assertEqual(second.status, "open")
        self.assertEqual(first.status, "close")
        self.assertEqual(self.partner_roy.dea_number, "AB1234563")

    def test_search_id_number_limited_to_context_partner(self):
        numbers = self.partner_number_obj.with_context(
            partner_id=self.partner_roy.id
        ).search([("category_id.code", "=", "DEA")])
        self.assertTrue(numbers)
        self.assertTrue(
            all(number.partner_id == self.partner_roy for number in numbers)
        )
        self.assertFalse(
            numbers.filtered(lambda number: number.partner_id == self.partner_john)
        )

    def test_sale_order_onchange_dea_number(self):
        dea = self.partner_roy.id_numbers.filtered(
            lambda number: number.category_id == self.dea_category_id
        )[:1]
        order = self.env["sale.order"].new({"dea_number_id": dea.id})
        order._onchange_dea_number_id()
        self.assertEqual(order.partner_id, self.partner_roy)
        empty_order = self.env["sale.order"].new({})
        empty_order._onchange_dea_number_id()
        self.assertFalse(empty_order.partner_id)
