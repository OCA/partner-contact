# Copyright  2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from psycopg2._psycopg import IntegrityError

from odoo.exceptions import UserError, ValidationError
from odoo.tests import common
from odoo.tools import mute_logger


class TestPartnerIdentificationBase(common.TransactionCase):
    def test_create_id_category(self):
        partner_id_category = self.env["res.partner.id_category"].create(
            {"code": "id_code", "name": "id_name"}
        )
        self.assertEqual(partner_id_category.name, "id_name")
        self.assertEqual(partner_id_category.code, "id_code")

    @mute_logger("odoo.sql_db")
    def test_update_partner_with_no_category(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Apik test",
                "email": "apik@test.example.com",
                "phone": "+33 601 020 304",
                "street": "Rue de la mairie",
                "city": "New York",
                "zip": "97648",
                "website": "https://test.exemple.com",
            }
        )

        self.assertEqual(len(partner.id_numbers), 0)
        # create without required category
        with self.assertRaises(IntegrityError):
            partner.write({"id_numbers": [(0, 0, {"name": "1234"})]})

    def test_update_partner_with_category(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Apik test",
                "email": "apik@test.example.com",
                "phone": "+33 601 020 304",
                "street": "Rue de la mairie",
                "city": "New York",
                "zip": "97648",
                "website": "https://test.exemple.com",
            }
        )

        partner_id_category = self.env["res.partner.id_category"].create(
            {"code": "new_code", "name": "new_name"}
        )
        # successful creation
        partner.write(
            {
                "id_numbers": [
                    (0, 0, {"name": "1234", "category_id": partner_id_category.id})
                ]
            }
        )
        self.assertEqual(len(partner.id_numbers), 1)
        self.assertEqual(partner.id_numbers.name, "1234")
        # delete
        partner.write({"id_numbers": [(5, 0, 0)]})
        self.assertEqual(len(partner.id_numbers), 0)


class TestPartnerCategoryValidation(common.TransactionCase):
    def test_partner_id_number_validation(self):
        partner_id_category = self.env["res.partner.id_category"].create(
            {
                "code": "id_code",
                "name": "id_name",
                "validation_code": """
if id_number.name != '1234':
    failed = True
""",
            }
        )
        partner = self.env["res.partner"].create(
            {
                "name": "Apik test",
                "email": "apik@test.example.com",
                "phone": "+33 601 020 304",
                "street": "Rue de la mairie",
                "city": "New York",
                "zip": "97648",
                "website": "https://test.exemple.com",
            }
        )
        with self.assertRaises(ValidationError), self.cr.savepoint():
            partner.write(
                {
                    "id_numbers": [
                        (0, 0, {"name": "01234", "category_id": partner_id_category.id})
                    ]
                }
            )
        partner.write(
            {
                "id_numbers": [
                    (0, 0, {"name": "1234", "category_id": partner_id_category.id})
                ]
            }
        )
        self.assertEqual(len(partner.id_numbers), 1)
        self.assertEqual(partner.id_numbers.name, "1234")

        partner_id_category2 = self.env["res.partner.id_category"].create(
            {
                "code": "id_code2",
                "name": "id_name2",
                "validation_code": """
if id_number.name != '1235':
    failed = True
""",
            }
        )
        # check that the constrains is also checked when we change the
        # associated category
        with self.assertRaises(ValidationError), self.cr.savepoint():
            partner.id_numbers.write({"category_id": partner_id_category2.id})

    def test_bad_validation_code(self):
        partner_id_category = self.env["res.partner.id_category"].create(
            {
                "code": "id_code",
                "name": "id_name",
                "validation_code": """
if id_number.name != '1234' #  missing :
    failed = True
""",
            }
        )
        partner = self.env["res.partner"].create(
            {
                "name": "Apik test",
                "email": "apik@test.example.com",
                "phone": "+33 601 020 304",
                "street": "Rue de la mairie",
                "city": "New York",
                "zip": "97648",
                "website": "https://test.exemple.com",
            }
        )
        with self.assertRaises(UserError):
            partner.write(
                {
                    "id_numbers": [
                        (0, 0, {"name": "1234", "category_id": partner_id_category.id})
                    ]
                }
            )

    def test_bad_validation_code_override(self):
        """It should allow a bad validation code if context overrides."""
        partner_id_category = self.env["res.partner.id_category"].create(
            {
                "code": "id_code",
                "name": "id_name",
                "validation_code": """
if id_number.name != '1234' #  missing :
    failed = True
""",
            }
        )
        partner = (
            self.env["res.partner"]
            .create(
                {
                    "name": "Apik test",
                    "email": "apik@test.example.com",
                    "phone": "+33 601 020 304",
                    "street": "Rue de la mairie",
                    "city": "New York",
                    "zip": "97648",
                    "website": "https://test.exemple.com",
                }
            )
            .with_context(id_no_validate=True)
        )
        partner.write(
            {
                "id_numbers": [
                    (0, 0, {"name": "1234", "category_id": partner_id_category.id})
                ]
            }
        )
