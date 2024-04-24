# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestBasePartnerTwoLine(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        partner_model = cls.env["res.partner"]
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

    def test_get_name(self):
        # Partner with name.
        name = self.child_partner_name.with_context(
            _two_lines_partner_address=True
        )._get_name()
        self.assertEqual(name, "Test Company Name\nTest Partner Name")
        # Partner without a name.
        name = self.child_partner_no_name.with_context(
            _two_lines_partner_address=True
        )._get_name()
        self.assertEqual(name, "Test Company Name\nInvoice Address")
