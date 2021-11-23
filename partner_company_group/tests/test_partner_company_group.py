# Copyright 2021 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import SingleTransactionCase
from odoo.exceptions import ValidationError


class TestProductManagedReplenishmentCost(SingleTransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env.ref('base.res_partner_3')
        cls.partner1 = cls.env.ref('base.res_partner_4')

    def test_01_create_partner(self):
        self.partner.company_group_id = self.partner1
        with self.assertRaises(ValidationError):
            self.partner.company_group_id = self.partner
