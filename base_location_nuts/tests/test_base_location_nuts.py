# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from requests.exceptions import HTTPError

from odoo.tests.common import Form, TransactionCase, new_test_user
from odoo.tools import mute_logger

from .test_nuts_request_results import create_response_error, create_response_ok

MOCK_PATH = "odoo.addons.base_location_nuts.wizard.nuts_import.requests.get"


class TestBaseLocationNuts(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestBaseLocationNuts, cls).setUpClass()
        cls.uid = new_test_user(
            cls.env,
            login="test-nuts-import-user",
            groups="base.group_partner_manager",
        )
        cls.nut_form = Form(cls.env["nuts.import"].with_user(cls.uid))
        cls.nut_wizard = cls.nut_form.save()
        with patch(MOCK_PATH, return_value=create_response_ok()):
            cls.nut_wizard.import_update_partner_nuts()
        cls.country_1 = cls.env["res.country"].search([("code", "=", "ES")])
        cls.country_2 = cls.env["res.country"].search([("code", "=", "PT")])
        cls.nuts_model = cls.env["res.partner.nuts"]
        cls.nuts1_2 = cls.nuts_model.search([("code", "=", "PT1a")])
        cls.nuts1_2.write({"country_id": cls.country_2})
        cls.nuts2_1 = cls.nuts_model.search([("code", "=", "ES2a")])
        cls.nuts1_2.write({"country_id": cls.country_2})
        cls.nuts3_1 = cls.nuts_model.search([("code", "=", "ES24a")])
        cls.nuts1_2.write({"country_id": cls.country_2})
        cls.nuts4_1 = cls.nuts_model.search([("code", "=", "ES243a")])
        cls.nuts1_2.write({"country_id": cls.country_2})
        cls.nuts4_2 = cls.nuts_model.search([("code", "=", "ES300a")])
        cls.nuts1_2.write({"country_id": cls.country_2})

        cls.partner = cls.env["res.partner"].create(
            {"name": "Test partner", "country_id": cls.country_1.id}
        )
        cls.state_1 = cls.env["res.country.state"].create(
            {"name": "Zaragoza Test", "code": "ZT", "country_id": cls.country_1.id}
        )
        cls.nuts4_1.state_id = cls.state_1
        cls.state_2 = cls.env["res.country.state"].create(
            {"name": "Madrid Test", "code": "MT", "country_id": cls.country_1.id}
        )
        cls.nuts4_2.state_id = cls.state_2
        cls.country_1.state_level = 4

    def test_onchange_nuts_country(self):
        self.partner.nuts1_id = self.nuts1_2
        self.partner._onchange_nuts1_id()
        self.assertEqual(self.partner.country_id, self.nuts1_2.country_id)

    def test_onchange_nuts(self):
        self.partner.country_id = self.country_2
        self.partner._onchange_country_id_base_location_nuts()
        self.assertEqual(self.partner.nuts1_id.country_id, self.partner.country_id)
        self.partner.nuts4_id = self.nuts4_1
        self.partner._onchange_nuts4_id()
        self.assertEqual(self.partner.country_id, self.country_1)
        self.assertEqual(self.partner.nuts3_id, self.nuts3_1)
        self.partner._onchange_nuts3_id()
        self.assertEqual(self.partner.nuts2_id, self.nuts2_1)
        self.partner._onchange_nuts2_id()
        self.assertEqual(self.partner.nuts1_id.country_id, self.country_1)
        self.partner.country_id = self.country_2
        self.partner._onchange_country_id_base_location_nuts()
        self.assertEqual(self.partner.country_id, self.nuts1_2.country_id)
        self.assertFalse(self.partner.nuts2_id)
        self.assertFalse(self.partner.nuts3_id)
        self.assertFalse(self.partner.nuts4_id)

    def test_onchange_states(self):
        self.partner.state_id = self.state_2
        self.partner.onchange_state_id_base_location_nuts()
        self.assertEqual(self.state_2, self.partner.nuts4_id.state_id)
        self.partner.state_id = self.state_1
        self.partner.onchange_state_id_base_location_nuts()
        self.assertEqual(self.state_1, self.partner.nuts4_id.state_id)
        self.partner._onchange_nuts4_id()
        self.assertEqual(self.partner.nuts3_id, self.nuts3_1)
        self.partner._onchange_nuts3_id()
        self.assertEqual(self.partner.nuts2_id, self.nuts2_1)
        self.partner._onchange_nuts2_id()
        self.assertEqual(self.partner.nuts1_id.country_id, self.country_1)

    @mute_logger("odoo.addons.base_location_nuts.wizard.nuts_import")
    @patch(MOCK_PATH, return_value=create_response_error())
    def test_download_exceptions(self, mock_request):
        """Tests request exceptions"""
        with self.assertRaises(HTTPError):
            self.nut_wizard.import_update_partner_nuts()

    def create_new_parent(self, orig_parent):
        new_parent = self.nuts_model.create(
            {
                "level": orig_parent.level,
                "code": "NEW" + orig_parent.code,
                "name": "New parent",
                "country_id": orig_parent.country_id.id,
                "not_updatable": False,
            }
        )
        return new_parent

    @patch(MOCK_PATH, return_value=create_response_ok())
    def test_no_update(self, mock_response):
        # Update a NUTS field
        orig_name = self.nuts4_2.name
        new_name = 2 * orig_name
        self.assertNotEqual(orig_name, new_name)

        # Update hierarchy creating a new parent
        orig_parent = self.nuts4_2.parent_id
        new_parent = self.create_new_parent(orig_parent)
        self.assertNotEqual(orig_parent, new_parent)

        # If the flag is False (default), updates will be overwritten
        # and the new parent deleted
        self.assertFalse(self.nuts4_2.not_updatable)
        self.assertFalse(new_parent.not_updatable)
        self.nuts4_2.name = new_name
        self.nuts4_2.parent_id = new_parent
        self.nut_wizard.import_update_partner_nuts()
        self.assertEqual(self.nuts4_2.name, orig_name)
        self.assertEqual(self.nuts4_2.parent_id, orig_parent)
        self.assertFalse(new_parent.exists())

        # New parent has been deleted by the import
        new_parent = self.create_new_parent(orig_parent)

        # If the flag is True, creation and updates will not be overwritten
        self.nuts4_2.not_updatable = True
        new_parent.not_updatable = True
        self.nuts4_2.name = new_name
        self.nuts4_2.parent_id = new_parent
        self.nut_wizard.import_update_partner_nuts()
        self.assertEqual(self.nuts4_2.name, new_name)
        self.assertEqual(self.nuts4_2.parent_id, new_parent)
        self.assertTrue(new_parent.exists())
