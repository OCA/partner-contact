# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from odoo.tests import TransactionCase


class TestPartnerContactOwnAddress(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Partner = cls.env["res.partner"]
        cls.company = cls.Partner.create(
            {
                "name": "Company",
                "is_company": True,
                "street": "Company Street 1",
                "city": "Company City",
            }
        )
        cls.colleague = cls.Partner.create(
            {
                "name": "Colleague",
                "parent_id": cls.company.id,
                "type": "contact",
                "own_address": False,
            }
        )
        cls.remote = cls.Partner.create(
            {
                "name": "Remote",
                "parent_id": cls.company.id,
                "type": "contact",
                "own_address": True,
                "street": "Home Street 1",
                "city": "Home City",
            }
        )

    def test_create_keeps_own_address(self):
        self.assertEqual(self.remote.street, "Home Street 1")
        self.assertEqual(self.company.street, "Company Street 1")

    def test_contact_address_does_not_change_company(self):
        self.remote.street = "Home Street 2"
        self.assertEqual(self.company.street, "Company Street 1")
        self.assertEqual(self.colleague.street, "Company Street 1")

    def test_company_address_does_not_change_contact(self):
        self.company.street = "Company Street 2"
        self.assertEqual(self.remote.street, "Home Street 1")
        self.assertEqual(self.colleague.street, "Company Street 2")

    def test_contact_without_option_still_syncs(self):
        self.colleague.street = "Company Street 3"
        self.assertEqual(self.company.street, "Company Street 3")
        self.assertEqual(self.remote.street, "Home Street 1")

    def test_address_field_added_by_another_module(self):
        partner_class = type(self.Partner)
        address_fields = partner_class._address_fields

        def _address_fields(self):
            return address_fields(self) + ["function"]

        with patch.object(partner_class, "_address_fields", _address_fields):
            self.remote.function = "Home Office"
            self.assertFalse(self.company.function)
            self.company.function = "Head Office"
            self.assertEqual(self.remote.function, "Home Office")
            self.assertEqual(self.colleague.function, "Head Office")

    def test_commercial_fields_still_sync(self):
        self.company.vat = "BE0477472701"
        self.assertEqual(self.remote.vat, "BE0477472701")
        other = self.Partner.create(
            {"name": "Other", "is_company": True, "vat": "BE0202239951"}
        )
        self.remote.parent_id = other
        self.assertEqual(self.remote.vat, "BE0202239951")

    def test_move_to_another_company_keeps_address(self):
        other = self.Partner.create(
            {"name": "Other", "is_company": True, "street": "Other Street 1"}
        )
        self.remote.parent_id = other
        self.assertEqual(self.remote.street, "Home Street 1")
        self.assertEqual(other.street, "Other Street 1")

    def test_untick_takes_company_address(self):
        self.remote.own_address = False
        self.assertEqual(self.remote.street, "Company Street 1")
        self.assertEqual(self.remote.city, "Company City")
        self.company.street = "Company Street 2"
        self.assertEqual(self.remote.street, "Company Street 2")

    def test_untick_and_change_type_keeps_address(self):
        self.remote.write({"own_address": False, "type": "invoice"})
        self.assertEqual(self.remote.street, "Home Street 1")
        self.assertEqual(self.remote.city, "Home City")

    def test_own_contacts_follow_contact_address(self):
        assistant = self.Partner.create(
            {
                "name": "Assistant",
                "parent_id": self.remote.id,
                "type": "contact",
                "own_address": False,
            }
        )
        self.assertEqual(assistant.street, "Home Street 1")
        self.remote.street = "Home Street 2"
        self.assertEqual(assistant.street, "Home Street 2")
        self.assertEqual(self.company.street, "Company Street 1")

    def test_first_contact_does_not_fill_company_address(self):
        company = self.Partner.create({"name": "Empty Company", "is_company": True})
        self.Partner.create(
            {
                "name": "First",
                "parent_id": company.id,
                "type": "contact",
                "own_address": True,
                "street": "Home Street 1",
            }
        )
        self.assertFalse(company.street)

    def test_import_keeps_own_address(self):
        result = self.Partner.load(
            ["name", "parent_id/.id", "type", "own_address", "street"],
            [["Imported", str(self.company.id), "contact", "1", "Home Street 9"]],
        )
        self.assertFalse(result["messages"])
        imported = self.Partner.browse(result["ids"])
        self.assertEqual(imported.street, "Home Street 9")
        self.assertFalse(imported.city)
        self.assertEqual(self.company.street, "Company Street 1")

    def test_import_keeps_address_defaults(self):
        country = self.env.ref("base.be")
        self.env["ir.default"].set("res.partner", "country_id", country.id)
        result = self.Partner.load(
            ["name", "parent_id/.id", "type", "own_address", "street"],
            [["Imported", str(self.company.id), "contact", "1", "Home Street 9"]],
        )
        imported = self.Partner.browse(result["ids"])
        self.assertEqual(imported.country_id, country)

    def test_import_first_contact_does_not_fill_company_address(self):
        company = self.Partner.create({"name": "Empty Company", "is_company": True})
        self.Partner.load(
            ["name", "parent_id/.id", "type", "own_address", "street"],
            [["Imported", str(company.id), "contact", "1", "Home Street 9"]],
        )
        self.assertFalse(company.street)

    def test_onchange_parent_keeps_own_address(self):
        other = self.Partner.create(
            {"name": "Other", "is_company": True, "street": "Other Street 1"}
        )
        remote = self.remote.new({"parent_id": other.id}, origin=self.remote)
        self.assertNotIn("street", remote.onchange_parent_id().get("value", {}))
        colleague = self.colleague.new({"parent_id": other.id}, origin=self.colleague)
        self.assertEqual(
            colleague.onchange_parent_id()["value"]["street"], "Other Street 1"
        )

    def test_address_label(self):
        self.assertEqual(self.remote.type_address_label, "Address")
        self.assertEqual(self.colleague.type_address_label, "Company Address")
