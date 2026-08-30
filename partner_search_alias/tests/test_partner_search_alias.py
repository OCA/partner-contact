# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree

from odoo.tests.common import TransactionCase


class TestPartnerAlias(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "search_alias": "alias",
            }
        )

    def test_name_search_with_alias(self):
        partners = self.env["res.partner"].name_search("alias")
        partner_ids = [partner[0] for partner in partners]
        # Ensure the search returns the created partner
        self.assertIn(
            self.partner.id,
            partner_ids,
            "The partner with search_alias 'alias' should be found.",
        )

    def test_get_view_search_filter_domain_modified(self):
        # Ensure that search filter include the search_alias.
        view = self.partner.get_view(view_type="search")
        xml = etree.XML(view["arch"])
        name_field = xml.xpath("//field[@name='name']")
        self.assertTrue(name_field, "Search view must contain name field")
        filter_domain = name_field[0].get("filter_domain", "")
        self.assertIn(
            "search_alias", filter_domain, "Filter domain must include 'search_alias'"
        )
