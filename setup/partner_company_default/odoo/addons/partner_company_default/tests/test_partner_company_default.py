# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import odoo.tests.common as common


class TestPartnerCompanyDefault(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env.ref("base.user_admin")

    def test_partner_company_default(self):
        # Check company of newly created partner
        partner = (
            self.env["res.partner"]
            .with_user(self.user.id)
            .with_context(test_partner_company_default=True)
            .create({"name": "Test Partner 1"})
        )
        self.assertEqual(partner.company_id, self.user.company_id)

        # Check company of the partner of newly created company
        company_fr = (
            self.env["res.company"]
            .with_user(self.user.id)
            .create(
                {
                    "name": "French company",
                    "currency_id": self.env.ref("base.EUR").id,
                    "country_id": self.env.ref("base.fr").id,
                }
            )
        )
        self.assertFalse(company_fr.partner_id.company_id)

        # Switch user's company and create a partner
        self.user.company_ids = [(4, company_fr.id)]
        self.user.company_id = company_fr.id
        partner = (
            self.env["res.partner"]
            .with_user(self.user.id)
            .with_context(test_partner_company_default=True)
            .create({"name": "Test Partner 2"})
        )
        self.assertEqual(partner.company_id, company_fr)
