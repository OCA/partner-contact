import json

from odoo import fields

from odoo.addons.base.tests.common import BaseCommon


class TestResCompanyProperty(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_1 = cls.env["res.company"].create(
            {
                "name": "Test Company 1",
            }
        )
        cls.company_2 = cls.env["res.company"].create(
            {
                "name": "Test Company 2",
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.ICP = cls.env["ir.config_parameter"].sudo()
        cls.test_definition = [
            {
                "name": "fe5039d0d3a11b01",
                "string": "Property 1",
                "type": "integer",
                "default": 50,
                "view_in_cards": True,
            }
        ]
        cls.new_definition = [
            {
                "name": "41776edf2cc662ee",
                "string": "Property 2",
                "type": "boolean",
                "default": True,
                "view_in_cards": True,
            }
        ]

    def test_compute_and_inverse_partner_properties_definition_company(self):
        """Test compute and inverse methods for syncing company partner properties
        with system parameters."""
        properties = fields.PropertiesDefinition()
        self.company_1.partner_properties_definition_company = (
            properties.convert_to_cache(
                json.dumps(self.test_definition), self.company_1
            )
        )
        saved_value = self.ICP.get_param(
            "partner_property.properties_definition_company"
        )
        saved_value_json = json.loads(saved_value)
        self.assertEqual(
            saved_value_json,
            self.test_definition,
            "Inverse method did not save the correct data",
        )
        self.company_1.partner_properties_definition_company = (
            properties.convert_to_cache(json.dumps(self.new_definition), self.company_1)
        )
        loaded_value = self.company_1.with_company(
            self.company_2
        ).partner_properties_definition_company
        loaded_cache = properties.convert_to_cache(loaded_value, self.company_2)
        expected_cache = properties.convert_to_cache(
            json.dumps(self.new_definition), self.company_2
        )
        self.assertEqual(
            loaded_cache,
            expected_cache,
            "Compute method did not load updated data from system parameters",
        )

    def test_compute_and_inverse_partner_properties_definition_person(self):
        """Test compute and inverse methods for syncing person partner properties
        with system parameters."""
        properties = fields.PropertiesDefinition()
        self.company_1.partner_properties_definition_person = (
            properties.convert_to_cache(
                json.dumps(self.test_definition), self.company_1
            )
        )
        saved_value = self.ICP.get_param(
            "partner_property.properties_definition_person"
        )
        saved_value_json = json.loads(saved_value)
        self.assertEqual(
            saved_value_json,
            self.test_definition,
            "Inverse method did not save the correct data",
        )
        self.company_1.partner_properties_definition_person = (
            properties.convert_to_cache(json.dumps(self.new_definition), self.company_1)
        )
        loaded_value = self.company_1.with_company(
            self.company_2
        ).partner_properties_definition_person
        loaded_cache = properties.convert_to_cache(loaded_value, self.company_2)
        expected_cache = properties.convert_to_cache(
            json.dumps(self.new_definition), self.company_2
        )
        self.assertEqual(
            loaded_cache,
            expected_cache,
            "Compute method did not load updated data from system parameters",
        )
