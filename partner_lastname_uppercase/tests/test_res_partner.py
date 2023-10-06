# Copyright 2023 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class LastnameUppercaseCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["ir.config_parameter"].sudo().set_param(
            "partner_lastname_uppercase.convert_lastnames_to_uppercase", True
        )

    def _create_partner(self):
        return self.env["res.partner"].create(
            {
                "firstname": "John",
                "lastname": "Doe",
            }
        )

    def _create_company(self, name=None):
        if name is None:
            name = "A Company"
        return self.env["res.partner"].create({"name": name, "is_company": True})

    def test_lastname_uppercased_on_create(self):
        partner = self._create_partner()
        self.assertEqual(partner.lastname, "DOE")

    def test_lastname_uppercased_on_write(self):
        partner = self._create_partner()
        partner.lastname = "Smith"
        self.assertEqual(partner.lastname, "SMITH")

    def test_removing_lastname(self):
        partner = self._create_partner()
        partner.lastname = False
        self.assertEqual(partner.lastname, False)

    def test_companys_name_not_uppercased_on_create(self):
        company = self._create_company()
        self.assertEqual(company.name, "A Company")
        self.assertEqual(company.lastname, "A Company")

    def test_companys_name_not_uppercased_on_write(self):
        company = self._create_company()
        new_name = "Another Company"
        company.name = new_name
        self.assertEqual(company.name, new_name)
        self.assertEqual(company.lastname, new_name)

    def test_existing_data_is_uppercased(self):
        brandon_freeman = self.env.ref("base.res_partner_address_15")
        azure_interior = self.env.ref("base.res_partner_12")
        freeman = brandon_freeman.lastname
        azure_interior_name = azure_interior.lastname
        self.env["res.partner"].uppercase_all_lastnames()
        self.assertEqual(brandon_freeman.lastname, freeman.upper())
        self.assertEqual(azure_interior.lastname, azure_interior_name)

    def test_setting_is_company_to_false(self):
        partner = self._create_partner()
        company_1 = self._create_company(name="A Company")
        company_2 = self._create_company(name="Another Company")

        partners = partner | company_1 | company_2
        partners.write({"is_company": False})
        self.assertEqual(partner.lastname, "DOE")
        self.assertEqual(company_1.lastname, "A COMPANY")
        self.assertEqual(company_2.lastname, "ANOTHER COMPANY")
