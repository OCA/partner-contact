# Copyright 2020 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
"""Test tabs visibility will be recomputed on partner views."""
from . import common


class TestPartnerViewActions(common.TestCommon):
    """Test the functionality in window action model."""

    post_install = True

    def test_non_partner_action(self):
        """Test action to open a view for a model that is not res.partner."""
        action_dict = self._read_model_action("res.country")
        self.assertIn("context", action_dict)
        self.assertIn("res_model", action_dict)

    def test_all_fields(self):
        """Test action to open a partner view and read all fields."""
        action_dict = self._read_model_action("res.partner")
        self.assertIn("context", action_dict)
        self.assertIn("res_model", action_dict)

    def test_some_fields(self):
        """Test action to open a partner view and read fields, including context."""
        action_dict = self._read_model_action(
            "res.partner", fields=["view_mode", "context"]
        )
        self.assertIn("context", action_dict)
        self.assertNotIn("res_model", action_dict)

    def test_no_context(self):
        """Test action to open a partner view and read fields, but not context."""
        action_dict = self._read_model_action(
            "res.partner", fields=["view_mode", "target"]
        )
        self.assertIn("view_mode", action_dict)
        self.assertNotIn("context", action_dict)
        self.assertNotIn("res_model", action_dict)

    def _read_model_action(self, model_name, fields=None):
        """Read a single action for a model and return a dict."""
        action_model = self.env["ir.actions.act_window"]
        action = action_model.search([("res_model", "=", model_name)], limit=1)
        self.assertTrue(bool(action))
        action_dicts = action.read(fields=fields)
        self.assertEqual(len(action_dicts), 1)
        return action_dicts[0]
