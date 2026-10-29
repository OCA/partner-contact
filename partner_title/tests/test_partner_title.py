# Copyright 2025 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestPartnerTitle(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Alexis de Lattre",
                "is_company": False,
                "title_id": cls.env.ref("partner_title.res_partner_title_mister").id,
            }
        )

    def test_name_with_title(self):
        self.assertEqual(
            self.partner.with_context(lang="en_US").name_with_title,
            "Mr. Alexis de Lattre",
        )
        self.partner.title_id = False
        self.assertEqual(self.partner.name_with_title, "Alexis de Lattre")
