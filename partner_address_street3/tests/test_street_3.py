# Copyright 2014-2020 Camptocamp SA
# @author: Nicolas Bessi
# Copyright 2016-2020 Akretion (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestStreet3(TransactionCase):
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

        post_init_hook(self.env.cr, None)
        us_country = self.env.ref("base.us")
        self.assertTrue("%(street3)s" in us_country.address_format)

    def test_uninstall(self):
        from ..hooks import uninstall_hook

        uninstall_hook(self.env.cr, None)
        us_country = self.env.ref("base.us")
        self.assertTrue("%(street3)s" not in us_country.address_format)
