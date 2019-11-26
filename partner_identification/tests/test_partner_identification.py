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
        partner_1 = self.env.ref("base.res_partner_1")
        self.assertEqual(len(partner_1.id_numbers), 0)
        # create without required category
        with self.assertRaises(IntegrityError):
            partner_1.write({"id_numbers": [(0, 0, {"name": "1234"})]})

    def test_update_partner_with_category(self):
        partner_1 = self.env.ref("base.res_partner_1")
        partner_id_category = self.env["res.partner.id_category"].create(
            {"code": "new_code", "name": "new_name"}
        )
        # successful creation
        partner_1.write(
            {
                "id_numbers": [
                    (0, 0, {"name": "1234", "category_id": partner_id_category.id})
                ]
            }
        )
        self.assertEqual(len(partner_1.id_numbers), 1)
        self.assertEqual(partner_1.id_numbers.name, "1234")
        # delete
        partner_1.write({"id_numbers": [(5, 0, 0)]})
        self.assertEqual(len(partner_1.id_numbers), 0)


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
        partner_1 = self.env.ref("base.res_partner_1")
        with self.assertRaises(ValidationError), self.cr.savepoint():
            partner_1.write(
                {
                    "id_numbers": [
                        (0, 0, {"name": "01234", "category_id": partner_id_category.id})
                    ]
                }
            )
        partner_1.write(
            {
                "id_numbers": [
                    (0, 0, {"name": "1234", "category_id": partner_id_category.id})
                ]
            }
        )
        self.assertEqual(len(partner_1.id_numbers), 1)
        self.assertEqual(partner_1.id_numbers.name, "1234")

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
            partner_1.id_numbers.write({"category_id": partner_id_category2.id})

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
        partner_1 = self.env.ref("base.res_partner_1")
        with self.assertRaises(UserError):
            partner_1.write(
                {
                    "id_numbers": [
                        (0, 0, {"name": "1234", "category_id": partner_id_category.id})
                    ]
                }
            )

    def test_bad_validation_code_override(self):
        """ It should allow a bad validation code if context overrides. """
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
        partner_1 = self.env.ref("base.res_partner_1").with_context(id_no_validate=True)
        partner_1.write(
            {
                "id_numbers": [
                    (0, 0, {"name": "1234", "category_id": partner_id_category.id})
                ]
            }
        )
