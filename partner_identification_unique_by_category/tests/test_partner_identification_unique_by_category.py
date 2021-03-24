# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestPartnerIdentificationUniqueByCategory(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.category_1 = cls.env["res.partner.id_category"].create(
            {"code": "UID", "name": "Group Id"}
        )
        cls.category_2 = cls.env["res.partner.id_category"].create(
            {"code": "GID", "name": "User Id"}
        )
        cls.partner_1 = cls.env.ref("base.res_partner_1")
        cls.partner_2 = cls.env.ref("base.res_partner_2")

    def test_id_creation(self):
        """Check Id unique (or not) validation."""
        self.category_1.has_unique_numbers = True
        self.env["res.partner.id_number"].create(
            {
                "name": "123",
                "category_id": self.category_1.id,
                "partner_id": self.partner_1.id,
            }
        )
        message = (
            "The Id 123 in the category Group Id could not be created "
            "because it already exists"
        )
        with self.assertRaisesRegex(ValidationError, message):
            self.env["res.partner.id_number"].create(
                {
                    "name": "123",
                    "category_id": self.category_1.id,
                    "partner_id": self.partner_2.id,
                }
            )
        # Allow to create same id in an other category
        self.env["res.partner.id_number"].create(
            {
                "name": "123",
                "category_id": self.category_2.id,
                "partner_id": self.partner_2.id,
            }
        )
        self.category_1.has_unique_numbers = False
        self.env["res.partner.id_number"].create(
            {
                "name": "123",
                "category_id": self.category_1.id,
                "partner_id": self.partner_2.id,
            }
        )

    def test_category_unique_activation(self):
        """Check there is no duplicate when enabling unicity."""
        self.env["res.partner.id_number"].create(
            {
                "name": "123456",
                "category_id": self.category_1.id,
                "partner_id": self.partner_1.id,
            }
        )
        self.category_1.has_unique_numbers = True
        self.category_1.has_unique_numbers = False
        self.env["res.partner.id_number"].create(
            {
                "name": "123456",
                "category_id": self.category_1.id,
                "partner_id": self.partner_2.id,
            }
        )
        message = (
            "The category Group Id can not be set to use unique numbers, "
            "because it already contains duplicates."
        )
        with self.assertRaisesRegex(ValidationError, message):
            self.category_1.has_unique_numbers = True
