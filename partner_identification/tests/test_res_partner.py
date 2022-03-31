# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests import common

from .fake_models import ResPartner, setup_test_model, teardown_test_model


class TestResPartner(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        setup_test_model(cls.env, ResPartner)
        bad_cat = cls.env["res.partner.id_category"].create(
            {"code": "another_code", "name": "another_name"}
        )
        cls.env["res.partner.id_number"].create(
            {
                "name": "Bad ID",
                "category_id": bad_cat.id,
                "partner_id": cls.env.user.partner_id.id,
            }
        )
        cls.partner_id_category = cls.env["res.partner.id_category"].create(
            {"code": "id_code", "name": "id_name"}
        )
        cls.partner = cls.env.ref("base.main_partner")
        cls.partner_id = cls.env["res.partner.id_number"].create(
            {
                "name": "Good ID",
                "category_id": cls.partner_id_category.id,
                "partner_id": cls.partner.id,
            }
        )

    @classmethod
    def tearDownClass(cls):
        teardown_test_model(cls.env, ResPartner)
        super().tearDownClass()

    def test_compute_identification(self):
        """It should set the proper field to the proper ID name."""
        self.partner._compute_identification("name", "id_code")
        self.assertEqual(self.partner.name, self.partner_id.name)

    def test_inverse_identification_saves(self):
        """It should set the ID name to the proper field value."""
        self.partner._inverse_identification("name", "id_code")
        self.assertEqual(self.partner_id.name, self.partner.name)

    def test_inverse_identification_creates_new_category(self):
        """It should create a new category of the type if non-existent."""
        self.partner._inverse_identification("name", "new_code_type")
        category = self.env["res.partner.id_category"].search(
            [("code", "=", "new_code_type")]
        )
        self.assertTrue(category)

    def test_inverse_identification_creates_new_id(self):
        """It should create a new ID of the type if non-existent."""
        category = self.env["res.partner.id_category"].create(
            {"code": "new_code_type", "name": "new_code_type"}
        )
        self.partner._inverse_identification("name", "new_code_type")
        identification = self.env["res.partner.id_number"].search(
            [("category_id", "=", category.id), ("partner_id", "=", self.partner.id)]
        )
        self.assertEqual(identification.name, self.partner.name)

    def test_inverse_identification_multi_exception(self):
        """It should not allow a write when multiple IDs of same type."""
        self.env["res.partner.id_number"].create(
            {
                "name": "Another ID",
                "category_id": self.partner_id_category.id,
                "partner_id": self.partner.id,
            }
        )
        with self.assertRaises(ValidationError):
            self.partner._inverse_identification("name", "id_code")

    def test_search_identification(self):
        """It should return the right record when searched by ID."""
        self.partner.social_security = "Test"
        partner = self.env["res.partner"].search([("social_security", "=", "Test")])
        self.assertEqual(partner, self.partner)
