# Copyright 2024 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/LGPL-3.0)

from odoo.addons.base.tests.common import BaseCommon


class TestResPartnerCategory(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_category = cls.env["res.partner.category"].create(
            {"name": "Test Category", "description": "This is a test description"}
        )

    def test_category_creation(self):
        """Test that a partner category is created correctly."""
        self.assertTrue(self.partner_category, "Partner category should be created.")
        self.assertEqual(self.partner_category.name, "Test Category")
        self.assertEqual(
            self.partner_category.description, "This is a test description"
        )

    def test_description_field_translation(self):
        """Test that the description field is translatable."""
        self.partner_category.with_context(
            lang="fr_FR"
        ).description = "Description en français"
        self.assertEqual(
            self.partner_category.with_context(lang="fr_FR").description,
            "Description en français",
        )
