# Copyright 2023 ForgeFlow, S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestCompanyDefaultPartnerPricelist(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.base_pricelist = self.env.ref("product.list0")
        self.pricelist_1 = self.env["product.pricelist"].create(
            {"name": "Test pricelist 1"}
        )
        self.pricelist_2 = self.env["product.pricelist"].create(
            {"name": "Test pricelist 2"}
        )
        self.partner = self.env["res.partner"].create({"name": "Test customer"})

    def test_company_default_partner_pricelist(self):
        """Test Company Default Partner Pricelist"""
        # By default, the pricelist of the partner is the first valid pricelist
        self.assertEqual(self.partner.property_product_pricelist, self.base_pricelist)
        # When the default is changed for the active company, the pricelist of
        # the partner is the one assigned to the current company
        self.env.company.default_property_product_pricelist = self.pricelist_2
        self.partner.invalidate_cache()
        self.assertEqual(self.partner.property_product_pricelist, self.pricelist_2)
        # Finally, when modified explicitly, the pricelist is the one
        # set by the user
        self.partner.property_product_pricelist = self.pricelist_1
        self.assertEqual(self.partner.property_product_pricelist, self.pricelist_1)
