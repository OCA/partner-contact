# Copyright 2014-2020 Camptocamp SA
# @author: Nicolas Bessi
# Copyright 2016-2020 Akretion (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestStreet3(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(
                cls.env.context,
                tracking_disable=True,
            )
        )

    def test_partner(self):
        # Test address_format has been updated on existing countries
        us_country = self.env.ref("base.us")
        self.assertTrue("%(street3)s" in us_country.address_format)

        homer = self.env["res.partner"].create(
            {
                "name": "Homer Simpson",
                "city": "Springfield",
                "street": "742 Evergreen Terrace",
                "street2": "Donut Lane",
                "street3": "Tho",
                "country_id": us_country.id,
            }
        )

        # test synchro of street3 on create
        bart = self.env["res.partner"].create(
            {
                "name": "Bart Simpson",
                "parent_id": homer.id,
                "type": "contact",
            }
        )
        self.assertEqual(bart.street3, "Tho")
        bart.street3 = "\n\n"
        bart_address = bart._display_address()
        self.assertTrue("\n\n" not in bart_address)

        # test synchro of street3 on write
        homer.write({"street3": "in OCA we trust"})
        self.assertEqual(bart.street3, "in OCA we trust")

    def test_post_init_hook(self):
        from ..hooks import post_init_hook

        post_init_hook(self.env)
        us_country = self.env.ref("base.us")
        self.assertTrue("%(street3)s" in us_country.address_format)

    def test_uninstall(self):
        from ..hooks import uninstall_hook

        uninstall_hook(self.env)
        us_country = self.env.ref("base.us")
        self.assertTrue("%(street3)s" not in us_country.address_format)

    def test_default_get_copies_street3_from_parent(self):
        parent = self.env["res.partner"].create(
            {
                "name": "Parent Company",
                "street": "123 Main St",
                "street2": "Floor 2",
                "street3": "Suite 100",
                "city": "Springfield",
                "country_id": self.env.ref("base.us").id,
            }
        )
        Partner = self.env["res.partner"]
        defaults = Partner.with_context(default_parent_id=parent.id).default_get(
            ["name", "street", "street2", "street3", "city", "parent_id"]
        )
        self.assertEqual(defaults.get("street3"), "Suite 100")
        self.assertEqual(defaults.get("street2"), "Floor 2")
        self.assertEqual(defaults.get("street"), "123 Main St")
        self.assertEqual(defaults.get("parent_id"), parent.id)

    def test_child_ids_context_contains_street3(self):
        view = self.env.ref("base.view_partner_form")
        arch = self.env["res.partner"].get_view(view.id, view_type="form")["arch"]
        self.assertIn("default_street3", arch)

    def test_get_view_various_scenarios(self):
        # 1. view_type != "form" (e.g. search view)
        search_view = self.env["ir.ui.view"].create(
            {
                "name": "test.partner.search",
                "model": "res.partner",
                "type": "search",
                "arch": """
                <search>
                    <field name="name"/>
                </search>
            """,
            }
        )
        res = self.env["res.partner"].get_view(search_view.id, view_type="search")
        self.assertNotIn("default_street3", res["arch"])

        # 2. form view without child_ids field (xpath yields no match)
        form_view_no_child_ids = self.env["ir.ui.view"].create(
            {
                "name": "test.partner.form.no.child.ids",
                "model": "res.partner",
                "type": "form",
                "arch": """
                <form>
                    <field name="name"/>
                </form>
            """,
            }
        )
        res = self.env["res.partner"].get_view(
            form_view_no_child_ids.id, view_type="form"
        )
        self.assertNotIn("default_street3", res["arch"])

        # 3. child_ids with no context attribute
        form_view_no_context = self.env["ir.ui.view"].create(
            {
                "name": "test.partner.form.no.context",
                "model": "res.partner",
                "type": "form",
                "arch": """
                <form>
                    <field name="child_ids"/>
                </form>
            """,
            }
        )
        res = self.env["res.partner"].get_view(
            form_view_no_context.id, view_type="form"
        )
        self.assertIn("context=\"{'default_street3': street3}\"", res["arch"])

        # 4. child_ids with context already containing default_street3
        form_view_existing = self.env["ir.ui.view"].create(
            {
                "name": "test.partner.form.existing",
                "model": "res.partner",
                "type": "form",
                "arch": """
                <form>
                    <field name="child_ids" context="{'default_street3': 'custom'}"/>
                </form>
            """,
            }
        )
        res = self.env["res.partner"].get_view(form_view_existing.id, view_type="form")
        self.assertIn("context=\"{'default_street3': 'custom'}\"", res["arch"])
        self.assertNotIn("street3}", res["arch"])  # No duplicate injection

        # 5. child_ids with context string not ending with } (e.g. parenthesized dict)
        form_view_invalid_context = self.env["ir.ui.view"].create(
            {
                "name": "test.partner.form.invalid.context",
                "model": "res.partner",
                "type": "form",
                "arch": """
                <form>
                    <field name="child_ids" context="({'default_parent_id': id})"/>
                </form>
            """,
            }
        )
        res = self.env["res.partner"].get_view(
            form_view_invalid_context.id, view_type="form"
        )
        self.assertNotIn("default_street3", res["arch"])
