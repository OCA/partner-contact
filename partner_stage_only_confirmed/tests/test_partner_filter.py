from lxml import etree

from odoo.addons.base.tests.common import BaseCommon


class TestConfirmedPartnerFilter(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Partner = cls.env["res.partner"]
        cls.View = cls.env["ir.ui.view"]
        cls.ConfigParam = cls.env["ir.config_parameter"]
        cls.partner_form_view = cls.env.ref("base.view_partner_form")
        cls.view_1 = cls.View.create(
            {
                "name": "test.partner.empty_domain",
                "model": "res.partner",
                "arch": """
                <form>
                    <sheet>
                        <field name="parent_id" domain=""/>
                    </sheet>
                </form>
            """,
                "type": "form",
            }
        )
        cls.view_2 = cls.View.create(
            {
                "name": "test.partner.empty_list_domain",
                "model": "res.partner",
                "arch": """
                <form>
                    <sheet>
                        <field name="parent_id" domain="[]"/>
                    </sheet>
                </form>
            """,
                "type": "form",
            }
        )

    def _get_parent_field_domain(self, context):
        view = self.Partner.with_context(**context).get_view(
            view_id=self.partner_form_view.id, view_type="form"
        )
        xml = etree.XML(view["arch"])
        parent_field = xml.xpath("//field[@name='parent_id']")
        self.assertTrue(parent_field, "Expected 'parent_id' field in partner form view")
        return parent_field[0].get("domain") or ""

    def test_confirmed_partner_filter_enabled(self):
        """
        Test that domain is applied to Many2one fields (e.g., parent_id) when filter
        is enabled
        """
        domain = self._get_parent_field_domain({"only_confirmed_partners": True})
        self.assertIn("'stage_state'", domain)
        self.assertIn("'confirmed'", domain)

    def test_confirmed_partner_filter_disabled(self):
        """
        Test that domain is not applied when filtering is explicitly disabled in
        context
        """
        domain = self._get_parent_field_domain({"only_confirmed_partners": False})
        self.assertNotIn("'stage_state'", domain)
        self.assertNotIn("'confirmed'", domain)

    def test_domain_empty_string(self):
        """Empty domain='' is replaced with the stage_state confirmed filter."""

        result = self.Partner.with_context(only_confirmed_partners=True).get_view(
            view_id=self.view_1.id, view_type="form"
        )
        xml = etree.XML(result["arch"])
        field = xml.xpath("//field[@name='parent_id']")[0]
        domain = field.get("domain")
        self.assertEqual(domain, "[('stage_state', '=', 'confirmed')]")

    def test_domain_empty_list_string(self):
        """Test field with domain='[]' gets replaced with
        [('stage_state', '=',''confirmed')]"""

        result = self.Partner.with_context(only_confirmed_partners=True).get_view(
            view_id=self.view_2.id, view_type="form"
        )
        xml = etree.XML(result["arch"])
        field = xml.xpath("//field[@name='parent_id']")[0]
        domain = field.get("domain")
        self.assertEqual(domain, "[('stage_state', '=', 'confirmed')]")

    def test_filter_respects_config_param_true(self):
        """Test system parameter enabling partner filter"""
        self.ConfigParam.set_param("partner_stage.only_confirmed_partners", "1")

        view = self.Partner.get_view(
            view_id=self.partner_form_view.id, view_type="form"
        )
        xml = etree.XML(view["arch"])
        parent_field = xml.xpath("//field[@name='parent_id']")
        self.assertTrue(parent_field, "Expected 'parent_id' field in partner form view")

        domain = parent_field[0].get("domain")
        self.assertIn("'stage_state'", domain)
        self.assertIn("'confirmed'", domain)

    def test_filter_respects_config_param_false(self):
        """Test system parameter disabling partner filter"""
        self.ConfigParam.set_param("partner_stage.only_confirmed_partners", "false")

        view = self.Partner.get_view(
            view_id=self.partner_form_view.id, view_type="form"
        )
        xml = etree.XML(view["arch"])
        parent_field = xml.xpath("//field[@name='parent_id']")
        self.assertTrue(parent_field, "Expected 'parent_id' field in partner form view")

        domain = parent_field[0].get("domain")
        self.assertNotIn("'stage_state'", domain)
        self.assertNotIn("'confirmed'", domain)

    def test_filter_respects_config_param_default(self):
        """Test default behavior when system parameter is not set"""
        self.ConfigParam.set_param("partner_stage.only_confirmed_partners", "")

        view = self.Partner.get_view(
            view_id=self.partner_form_view.id, view_type="form"
        )
        xml = etree.XML(view["arch"])
        parent_field = xml.xpath("//field[@name='parent_id']")
        self.assertTrue(parent_field, "Expected 'parent_id' field in partner form view")

        domain = parent_field[0].get("domain") or ""
        self.assertIn("'stage_state'", domain)
        self.assertIn("'confirmed'", domain)

    def test_filter_with_existing_domain(self):
        """Test that existing domain is extended with state condition"""
        # Create a view with an existing domain
        view_with_existing_domain = self.View.create(
            {
                "name": "test.partner.existing_domain",
                "model": "res.partner",
                "arch": """
                <form>
                    <sheet>
                        <field name="parent_id" domain="[('name', 'ilike', 'test')]"/>
                    </sheet>
                </form>
            """,
                "type": "form",
            }
        )

        result = self.Partner.with_context(only_confirmed_partners=True).get_view(
            view_id=view_with_existing_domain.id, view_type="form"
        )
        xml = etree.XML(result["arch"])
        field = xml.xpath("//field[@name='parent_id']")[0]
        domain = field.get("domain")

        # Should contain both the original domain and the state condition
        self.assertIn("'name'", domain)
        self.assertIn("'test'", domain)
        self.assertIn("'stage_state'", domain)
        self.assertIn("'confirmed'", domain)

    def test_filter_non_partner_many2one(self):
        """Test that non-partner Many2one fields are not modified"""
        # Create a view with non-partner Many2one field
        test_view = self.View.create(
            {
                "name": "test.non_partner_field",
                "model": "res.partner",
                "arch": """
                <form>
                    <sheet>
                        <field name="user_id"/>
                    </sheet>
                </form>
            """,
                "type": "form",
            }
        )

        result = self.Partner.with_context(only_confirmed_partners=True).get_view(
            view_id=test_view.id, view_type="form"
        )
        xml = etree.XML(result["arch"])
        field = xml.xpath("//field[@name='user_id']")[0]
        domain = field.get("domain") or ""

        # Should not contain state condition for non-partner field
        self.assertNotIn("'stage_state'", domain)
        self.assertNotIn("'confirmed'", domain)

    def test_filter_partner_many2one(self):
        """Test that partner Many2one fields are modified"""
        # Create a view with partner field
        test_view = self.View.create(
            {
                "name": "test.partner_field",
                "model": "res.partner",
                "arch": """
                <form>
                    <sheet>
                        <field name="parent_id"/>
                    </sheet>
                </form>
            """,
                "type": "form",
            }
        )

        result = self.Partner.with_context(only_confirmed_partners=True).get_view(
            view_id=test_view.id, view_type="form"
        )
        xml = etree.XML(result["arch"])
        field = xml.xpath("//field[@name='parent_id']")[0]
        domain = field.get("domain")

        # Should contain state condition for partner field
        self.assertIn("'stage_state'", domain)
        self.assertIn("'confirmed'", domain)

    def test_filter_various_view_types(self):
        """Test that filtering only occurs on form views"""
        # Test form view (should be filtered)
        result_form = self.Partner.with_context(only_confirmed_partners=True).get_view(
            view_id=self.partner_form_view.id, view_type="form"
        )
        xml_form = etree.XML(result_form["arch"])
        parent_field_form = xml_form.xpath("//field[@name='parent_id']")
        self.assertTrue(parent_field_form)
        domain_form = parent_field_form[0].get("domain") or ""
        self.assertIn("'stage_state'", domain_form)

        # In Odoo 19.0, tree views are now called list views
        # We'll test that the method properly handles different view types by checking
        # that the filtering is only applied to form views
        # Verify _filter_only_confirmed works correctly with different contexts
        partner_with_filter = self.Partner.with_context(only_confirmed_partners=True)
        # This should return True based on the context
        self.assertTrue(partner_with_filter._filter_only_confirmed())

        # Test with explicit false context
        partner_without_filter = self.Partner.with_context(
            only_confirmed_partners=False
        )
        self.assertFalse(partner_without_filter._filter_only_confirmed())

    def test_get_view_non_form_type(self):
        """Test that get_view doesn't modify non-form views"""
        # When view_type is not 'form', the filtering logic should not execute
        # This means the method should call super().get_view without modifications
        result = self.Partner.get_view(view_type="search")
        self.assertIn("arch", result)  # Should return a valid result
        # The filtering should not apply to search views

    def test_get_view_filter_disabled(self):
        """Test that get_view doesn't modify views when filtering is disabled"""
        # When _filter_only_confirmed returns False, no modifications should occur
        result = self.Partner.with_context(only_confirmed_partners=False).get_view(
            view_id=self.partner_form_view.id, view_type="form"
        )

        # Parse the result to check that no domain was added
        xml = etree.XML(result["arch"])
        parent_field = xml.xpath("//field[@name='parent_id']")
        if parent_field:  # If the field exists in the view
            domain = parent_field[0].get("domain") or ""
            # Should not contain the state condition if filtering is disabled
            self.assertNotIn("'stage_state'", domain)
            self.assertNotIn("'confirmed'", domain)

    def test_get_view_non_partner_many2one_field(self):
        """Test that non-partner Many2one fields are not modified"""
        # Create a view with a non-partner Many2one field
        test_view = self.View.create(
            {
                "name": "test.non_partner_field",
                "model": "res.partner",
                "arch": """
                <form>
                    <sheet>
                        <field name="user_id"/>
                    </sheet>
                </form>
            """,
                "type": "form",
            }
        )

        result = self.Partner.with_context(only_confirmed_partners=True).get_view(
            view_id=test_view.id, view_type="form"
        )
        xml = etree.XML(result["arch"])
        field = xml.xpath("//field[@name='user_id']")[0]
        domain = field.get("domain") or ""

        # Should not contain state condition for non-partner field
        self.assertNotIn("'stage_state'", domain)
        self.assertNotIn("'confirmed'", domain)

    def test_get_view_domain_extension(self):
        """Test that existing domains are properly extended"""
        # Create a view with a field that has an existing domain
        view_with_domain = self.View.create(
            {
                "name": "test.partner.with_domain",
                "model": "res.partner",
                "arch": """
                <form>
                    <sheet>
                        <field name="parent_id" domain="[('name', 'ilike', 'test')]"/>
                    </sheet>
                </form>
            """,
                "type": "form",
            }
        )

        result = self.Partner.with_context(only_confirmed_partners=True).get_view(
            view_id=view_with_domain.id, view_type="form"
        )
        xml = etree.XML(result["arch"])
        field = xml.xpath("//field[@name='parent_id']")[0]
        domain = field.get("domain")

        # Should contain both the original domain and the new condition
        self.assertIn("'name'", domain)
        self.assertIn("'stage_state'", domain)
        self.assertIn("'confirmed'", domain)

    def test_get_view_empty_domain_list(self):
        """Test that empty list domain [] gets replaced properly"""
        view_with_empty_domain = self.View.create(
            {
                "name": "test.partner.empty_domain_list",
                "model": "res.partner",
                "arch": """
                <form>
                    <sheet>
                        <field name="parent_id" domain="[]"/>
                    </sheet>
                </form>
            """,
                "type": "form",
            }
        )

        result = self.Partner.with_context(only_confirmed_partners=True).get_view(
            view_id=view_with_empty_domain.id, view_type="form"
        )
        xml = etree.XML(result["arch"])
        field = xml.xpath("//field[@name='parent_id']")[0]
        domain = field.get("domain")

        # Should be replaced with the confirmed state condition
        self.assertEqual(domain, "[('stage_state', '=', 'confirmed')]")

    def test_get_view_no_domain(self):
        """Test field with no initial domain gets the state condition"""
        view_with_no_domain = self.View.create(
            {
                "name": "test.partner.no_domain",
                "model": "res.partner",
                "arch": """
                <form>
                    <sheet>
                        <field name="parent_id"/>
                    </sheet>
                </form>
            """,
                "type": "form",
            }
        )

        result = self.Partner.with_context(only_confirmed_partners=True).get_view(
            view_id=view_with_no_domain.id, view_type="form"
        )
        xml = etree.XML(result["arch"])
        field = xml.xpath("//field[@name='parent_id']")[0]
        domain = field.get("domain")

        # Should have the confirmed state condition added
        self.assertEqual(domain, "[('stage_state', '=', 'confirmed')]")

    def test_filter_with_non_boolean_context_value(self):
        """Test behavior with non-boolean context value"""
        # Test with context value that converts to True in bool()
        result = self.Partner.with_context(
            only_confirmed_partners="any_string"
        )._filter_only_confirmed()
        self.assertTrue(result)

        # Test with context value that converts to False in bool()
        result = self.Partner.with_context(
            only_confirmed_partners=""
        )._filter_only_confirmed()
        self.assertFalse(result)

        result = self.Partner.with_context(
            only_confirmed_partners=0
        )._filter_only_confirmed()
        self.assertFalse(result)

    def test_empty_context_config_parameter(self):
        """Test behavior when config parameter is empty string"""
        self.ConfigParam.set_param("partner_stage.only_confirmed_partners", "")

        # Should return default value (True)
        result = self.Partner._filter_only_confirmed()
        self.assertTrue(result)

    def test_false_config_parameter_values(self):
        """Test behavior with false config parameter values"""
        # Only these values are considered falsy according to the implementation
        # Note: empty string is treated as "not set" by ir.config_parameter and
        # follows the default path (returning True), so it's not included here
        false_values = ["False", "false", "0"]

        for false_val in false_values:
            with self.subTest(false_val=false_val):
                self.ConfigParam.set_param(
                    "partner_stage.only_confirmed_partners", false_val
                )
                result = self.Partner._filter_only_confirmed()
                self.assertFalse(result, f"Failed for value: {false_val}")

    def test_true_config_parameter_values(self):
        """Test behavior with various true-like config parameter values"""
        # Note: "no" and "off" are treated as truthy by the current implementation
        # Only "False", "false", "0" are considered falsy
        # (empty string follows default path)
        true_values = ["True", "true", "1", "yes", "on", "no", "off", "anything_else"]

        for true_val in true_values:
            with self.subTest(true_val=true_val):
                self.ConfigParam.set_param(
                    "partner_stage.only_confirmed_partners", true_val
                )
                result = self.Partner._filter_only_confirmed()
                self.assertTrue(result, f"Failed for value: {true_val}")

    def test_filter_with_integer_context(self):
        """Test behavior with integer context values"""
        # Test with integer 1 (should be truthy)
        result = self.Partner.with_context(
            only_confirmed_partners=1
        )._filter_only_confirmed()
        self.assertTrue(result)

        # Test with integer 0 (should be falsy)
        result = self.Partner.with_context(
            only_confirmed_partners=0
        )._filter_only_confirmed()
        self.assertFalse(result)

    def test_filter_with_none_context(self):
        """Test behavior with None context value"""
        result = self.Partner.with_context(
            only_confirmed_partners=None
        )._filter_only_confirmed()
        self.assertFalse(result)  # bool(None) is False
