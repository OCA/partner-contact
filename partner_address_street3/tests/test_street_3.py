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

    def test_default_get_copies_street3_from_default_parent_id(self):
        """Replicate the "Add in Contacts & Addresses" inline form context.

        Odoo passes ``default_parent_id`` in the context when the inline
        ``child_ids`` form is opened from a company contact, so ``default_get``
        must pre-fill the address fields (including ``street3``) from that
        parent.
        """
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
        values = (
            self.env["res.partner"]
            .with_context(default_parent_id=parent.id, default_type="contact")
            .default_get(["street", "street2", "street3", "city"])
        )
        self.assertEqual(values.get("street3"), "Suite 100")
        self.assertEqual(values.get("street2"), "Floor 2")
        self.assertEqual(values.get("street"), "123 Main St")
        self.assertEqual(values.get("city"), "Springfield")

    def test_default_get_does_not_overwrite_explicit_value(self):
        """An explicit default must win over the parent's value."""
        parent = self.env["res.partner"].create(
            {"name": "Parent", "street3": "From parent"}
        )
        values = (
            self.env["res.partner"]
            .with_context(
                default_parent_id=parent.id,
                default_type="contact",
                default_street3="Explicit",
            )
            .default_get(["street3"])
        )
        self.assertEqual(values.get("street3"), "Explicit")

    def test_default_get_no_parent(self):
        values = (
            self.env["res.partner"]
            .with_context(default_type="contact")
            .default_get(["street3"])
        )
        self.assertNotIn("street3", values)
