# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestBasePartnerTwoLine(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        partner_model = cls.env["res.partner"].with_context(
            _two_lines_partner_address=True
        )
        partner = partner_model.create(
            {"name": "Test Company Name", "company_type": "company"}
        )
        cls.child_partner_name = partner_model.create(
            {
                "name": "Test Partner Name",
                "type": "invoice",
                "parent_id": partner.id,
            }
        )
        cls.child_partner_no_name = partner_model.create(
            {
                "name": "",
                "type": "invoice",
                "parent_id": partner.id,
            }
        )

        partner_2 = partner_model.create(
            {"name": "Test Company, LTD", "company_type": "company"}
        )

        cls.child_partner_name_2 = partner_model.create(
            {
                "name": "Test Partner Name 2",
                "type": "invoice",
                "parent_id": partner_2.id,
            }
        )

    def test_get_name(self):
        # Partner with name.
        self.assertEqual(
            self.child_partner_name.display_name, "Test Company Name\nTest Partner Name"
        )

        self.assertEqual(
            self.child_partner_name_2.display_name,
            "Test Company, LTD\nTest Partner Name 2",
        )

        # Partner without a name.
        self.assertEqual(
            self.child_partner_no_name.display_name,
            "Test Company Name\nInvoice Address",
        )
