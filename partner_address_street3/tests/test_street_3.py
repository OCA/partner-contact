# © 2014-2016 Camptocamp SA
# @author: Nicolas Bessi
# © 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestStreet3(TransactionCase):
    def setUp(self):
        super().setUp()
        self.us_country = self.env.ref("base.us")
        self.homer = self.env["res.partner"].create(
            {
                "name": "Homer Simpson",
                "city": "Springfield",
                "street": "742 Evergreen Terrace",
                "street2": "Donut Lane",
                "street3": "Tho",
                "country_id": self.us_country.id,
            }
        )

    def test_partner(self):
        # Test address_format has been updated on existing countries
        self.assertTrue("%(street3)s" in self.us_country.address_format)
        # test synchro of street3 on create
        bart = self.env["res.partner"].create(
            {"name": "Bart Simpson", "parent_id": self.homer.id, "type": "contact"}
        )
        self.assertEqual(bart.street3, "Tho")

        # test synchro of street3 on write
        self.homer.write({"street3": "in OCA we trust"})
        self.assertEqual(bart.street3, "in OCA we trust")

    def test_street3_in_address(self):
        self.assertEqual(
            self.homer.contact_address,
            "742 Evergreen Terrace\nDonut Lane\nTho\nSpringfield  \nUnited States",
        )
        self.homer.street3 = False
        self.assertEqual(
            self.homer.contact_address,
            "742 Evergreen Terrace\nDonut Lane\nSpringfield  \nUnited States",
        )
