# Copyright 2017 Grant Thornton Spain - Ismael Calvo <ismael.calvo@es.gt.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from unittest.mock import patch

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase

from odoo.addons.partner_vat_unique.models.res_partner import ResPartner


class TestVatUnique(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestVatUnique, cls).setUpClass()
        cls.partner_model = cls.env["res.partner"]
        cls.partner = cls.partner_model.create(
            {"name": "Test partner", "vat": "ESA12345674"}
        )

    def test_duplicated_vat_creation(self):
        with self.assertRaises(ValidationError):
            self.partner_model.with_context(test_vat=True, xmlrpc=True).create(
                {"name": "Second partner", "vat": "ESA12345674"}
            )

    def test_duplicate_partner(self):
        partner_copied = self.partner.copy()
        self.assertFalse(partner_copied.vat)

    @patch.object(ResPartner, "_check_vat_unique")
    def test_check_vat_unique_called_with_xmlrpc(self, _check_vat_unique_mock):
        self.partner_model.with_context(xmlrpc=True).create(
            {"name": "Third partner", "vat": "BE0477472701"}
        )
        self.partner_model.with_context(xmlrpc=True).create(
            {"name": "Multiple partner 01", "vat": "BE0477472722"}
        )
        self.partner_model.with_context(xmlrpc=True).create(
            {"name": "Third partner copy", "vat": "BE0477472701"}
        )
        _check_vat_unique_mock.assert_called_once()
