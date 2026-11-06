# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L. - Jairo Llopis.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

"""Test default values for models."""

from odoo.tests import TransactionCase


class PersonCase(TransactionCase):
    """Test ``res.partner`` when it is a person."""

    context = {"default_is_company": False}  # noqa: RUF012
    model = "res.partner"

    def setUp(self):
        super().setUp()
        self.good_values = {
            "firstname": "Núñez",
            "lastname": "Fernán",
            "is_company": self.context["default_is_company"],
        }
        self.good_values["name"] = "{} {}".format(
            self.good_values["firstname"], self.good_values["lastname"]
        )
        self.values = self.good_values.copy()

    def common_operations(self):
        self.record = (
            self.env[self.model].with_context(**self.context).create(self.values)
        )
        for key, value in self.good_values.items():
            self.assertEqual(self.record[key], value, f"Checking key {key}")

    def test_no_name(self):
        """Name is calculated."""
        del self.values["name"]
        self.common_operations()

    def test_wrong_name_value(self):
        """Wrong name value is ignored, name is calculated."""
        self.values["name"] = "BÄD"
        self.common_operations()

    def test_wrong_name_context(self):
        """Wrong name context is ignored, name is calculated."""
        del self.values["name"]
        self.context["default_name"] = "BÄD"
        self.common_operations()

    def test_wrong_name_value_and_context(self):
        """Wrong name value and context is ignored, name is calculated."""
        self.values["name"] = "BÄD1"
        self.context["default_name"] = "BÄD2"
        self.common_operations()


class CompanyCase(TransactionCase):
    """Test ``res.partner`` when it is a company."""

    def test_create_company(self):
        """A partner with a Tax ID is a company: its name is not split."""
        name = "Sôme Company"
        partner = self.env["res.partner"].create({"name": name, "vat": "BE0477472701"})
        self.assertTrue(partner.is_company)
        self.assertEqual(partner.name, name)
        self.assertEqual(partner.lastname, name)
        self.assertFalse(partner.firstname)

    def test_create_company_contact(self):
        """A contact of a company is never a company, its name is split."""
        company = self.env["res.partner"].create(
            {"name": "Sôme Company", "vat": "BE0477472701"}
        )
        partner = self.env["res.partner"].create(
            {"name": "Fïrst Läst", "vat": "BE0477472701", "parent_id": company.id}
        )
        self.assertFalse(partner.is_company)
        self.assertEqual(partner.firstname, "Fïrst")
        self.assertEqual(partner.lastname, "Läst")
