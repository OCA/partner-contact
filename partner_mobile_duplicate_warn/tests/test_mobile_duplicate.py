# Copyright 2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestResPartner(TransactionCase):
    def setUp(self):
        super().setUp()
        self.fr_country_id = self.env.ref("base.fr").id
        self.partner_simple = self.env["res.partner"].create(
            {
                "name": "Alexia Payet",
                "mobile": " +33699887766 ",
                "country_id": self.fr_country_id,
            }
        )
        self.partner_simple._onchange_mobile_validation()
        self.company1_id = self.env.ref("base.main_company").id
        partner_company = self.env["res.partner"].create(
            {
                "name": "Test Company",
                "is_company": True,
                "country_id": self.env.ref("base.fr").id,
            }
        )
        self.company2_id = (
            self.env["res.company"]
            .create(
                {
                    "name": "Test Company",
                    "partner_id": partner_company.id,
                    "currency_id": self.env.ref("base.EUR").id,
                }
            )
            .id
        )

    def test_partner_duplicate_simple(self):
        partner1 = self.env["res.partner"].create(
            {
                "name": "Test regular",
                "mobile": "06 99 88 77 65",
                "country_id": self.fr_country_id,
            }
        )
        partner1._onchange_mobile_validation()
        self.assertFalse(partner1.same_mobile_partner_id)
        partner1.write({"mobile": " 06 99 88 77 66"})
        partner1._onchange_mobile_validation()
        self.assertEqual(partner1.same_mobile_partner_id, self.partner_simple)

    def test_partner_duplicate_multi_company(self):
        partner_company1 = self.env["res.partner"].create(
            {
                "name": "Toto",
                "mobile": "+33 6 11 22 33 44",
                "company_id": self.company1_id,
            }
        )
        partner_company2 = self.env["res.partner"].create(
            {
                "name": "Toto",
                "mobile": "+33 6 11 22 33 44",
                "company_id": self.company2_id,
            }
        )
        self.assertFalse(partner_company1.same_mobile_partner_id)
        self.assertFalse(partner_company2.same_mobile_partner_id)
        partner_company2.write({"company_id": False})
        self.assertEqual(partner_company2.same_mobile_partner_id, partner_company1)
