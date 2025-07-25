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
        self.assertIn("'state'", domain)
        self.assertIn("'confirmed'", domain)

    def test_confirmed_partner_filter_disabled(self):
        """
        Test that domain is not applied when filtering is explicitly disabled in
        context
        """
        domain = self._get_parent_field_domain({"only_confirmed_partners": False})
        self.assertNotIn("'state'", domain)
        self.assertNotIn("'confirmed'", domain)

    def test_domain_empty_string(self):
        """Test field with domain='' gets replaced with [('state', '=', 'confirmed')]"""

        result = self.Partner.with_context(only_confirmed_partners=True).get_view(
            view_id=self.view_1.id, view_type="form"
        )
        xml = etree.XML(result["arch"])
        field = xml.xpath("//field[@name='parent_id']")[0]
        domain = field.get("domain")
        self.assertEqual(domain, "[('state', '=', 'confirmed')]")

    def test_domain_empty_list_string(self):
        """Test field with domain='[]' gets replaced with
        [('state', '=',''confirmed')]"""

        result = self.Partner.with_context(only_confirmed_partners=True).get_view(
            view_id=self.view_2.id, view_type="form"
        )
        xml = etree.XML(result["arch"])
        field = xml.xpath("//field[@name='parent_id']")[0]
        domain = field.get("domain")
        self.assertEqual(domain, "[('state', '=', 'confirmed')]")

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
        self.assertIn("'state'", domain)
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
        self.assertNotIn("'state'", domain)
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
        self.assertIn("'state'", domain)
        self.assertIn("'confirmed'", domain)
