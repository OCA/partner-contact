# Copyright 2024 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestPartnerBankAccountTypeConstraint(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.partner1 = cls.env["res.partner"].create({"name": "Alexis de Lattre"})

    def test_regular_create_bank_account(self):
        pbank1 = self.env["res.partner.bank"].create(
            {
                "acc_type_manual": "bank",
                "acc_number": "0232093729",
                "partner_id": self.partner1.id,
            }
        )
        self.assertTrue(pbank1)

    def test_iban_create_bank_account(self):
        acc_types = self.env["res.partner.bank"].get_supported_account_types()
        if any([x[0] == "iban" for x in acc_types]):
            # create valid IBAN
            pbank2 = self.env["res.partner.bank"].create(
                {
                    "acc_type_manual": "iban",
                    "acc_number": "FR26 5454 7777 3434 6262 8976 789",
                    "partner_id": self.partner1.id,
                }
            )
            self.assertTrue(pbank2)
            # fail to create bad IBAN
            with self.assertRaises(ValidationError):
                self.env["res.partner.bank"].create(
                    {
                        "acc_type_manual": "iban",
                        "acc_number": "NOT_AN_IBAN",
                        "partner_id": self.partner1.id,
                    }
                )
