# Copyright 2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestResPartner(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.partner_simple = cls.env["res.partner"].create(
            {
                "name": "Alexia Payet",
                "email": "alexia.payet@akretion.com",
            }
        )
        cls.partner_space_start = cls.env["res.partner"].create(
            {
                "name": "Alexia Payet",
                "email": " alexia.payet@videolan.org",
            }
        )
        cls.partner_space_end = cls.env["res.partner"].create(
            {
                "name": "Alexia Payet",
                "email": "alexia.payet@via.ecp.fr ",
            }
        )
        cls.company1_id = cls.env.ref("base.main_company").id
        partner_company = cls.env["res.partner"].create(
            {
                "name": "Test Company",
                "is_company": True,
                "country_id": cls.env.ref("base.fr").id,
            }
        )
        cls.company2_id = (
            cls.env["res.company"]
            .create(
                {
                    "name": "Test Company",
                    "partner_id": partner_company.id,
                    "currency_id": cls.env.ref("base.EUR").id,
                }
            )
            .id
        )

    def test_partner_duplicate_simple(self):
        partner1 = self.env["res.partner"].create(
            {
                "name": "Test regular",
                "email": "alexis.payet@akretion.com",
            }
        )
        self.assertFalse(partner1.same_email_partner_id)
        partner1.write({"email": "alexia.payet@akretion.com"})
        self.assertEqual(partner1.same_email_partner_id, self.partner_simple)

    def test_partner_duplicate_spaces_caps(self):
        partner2 = self.env["res.partner"].create(
            {
                "name": "Test space",
                "email": "alexia.payet@videolan.org",
            }
        )
        self.assertEqual(partner2.same_email_partner_id, self.partner_space_start)
        partner2.write({"email": "alexia.payet@videolan.org "})
        self.assertEqual(partner2.same_email_partner_id, self.partner_space_start)
        partner2.write({"email": " alexia.payet@videolan.org"})
        self.assertEqual(partner2.same_email_partner_id, self.partner_space_start)
        partner2.write({"email": " Alexia.Payet@videolan.org "})
        self.assertEqual(partner2.same_email_partner_id, self.partner_space_start)
        partner2.write({"email": "Alexia.Pazet@videolan.org"})
        self.assertFalse(partner2.same_email_partner_id)
        partner3 = self.env["res.partner"].create(
            {
                "name": "Test space2",
                "email": "Alexia.Payet@via.ecp.fr",
            }
        )
        self.assertEqual(partner3.same_email_partner_id, self.partner_space_end)
        partner3.write({"email": " Alexia.Payet@via.ecp.fr"})
        self.assertEqual(partner3.same_email_partner_id, self.partner_space_end)
        partner3.write({"email": " Alexia.Payet@Via.Ecp.Fr "})
        self.assertEqual(partner3.same_email_partner_id, self.partner_space_end)

    def test_partner_duplicate_multi_company(self):
        partner_company1 = self.env["res.partner"].create(
            {
                "name": "Toto",
                "email": "alexandra.payet@via.ecp.fr",
                "company_id": self.company1_id,
            }
        )
        partner_company2 = self.env["res.partner"].create(
            {
                "name": "Toto",
                "email": "alexandra.payet@via.ecp.fr",
                "company_id": self.company2_id,
            }
        )
        self.assertFalse(partner_company1.same_email_partner_id)
        self.assertFalse(partner_company2.same_email_partner_id)
        partner_company2.write({"company_id": False})
        self.assertEqual(partner_company2.same_email_partner_id, partner_company1)

    def test_partner_duplicate_parent_child(self):
        parent_partner = self.env["res.partner"].create(
            {
                "name": "Rocket Corp",
                "is_company": True,
                "email": "contact@rocket.com",
            }
        )
        child_partner = self.env["res.partner"].create(
            {
                "name": "M. Dupont",
                "is_company": False,
                "parent_id": parent_partner.id,
                "email": "contact@rocket.com",
            }
        )
        self.assertFalse(parent_partner.same_email_partner_id)
        self.assertFalse(child_partner.same_email_partner_id)
