# Copyright 2023 ForgeFlow, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError

from odoo.addons.base.tests.common import BaseCommon


class TestResPartnerCategory(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create base test categories
        cls.category_parent = cls.env["res.partner.category"].create(
            {
                "name": "Parent Category",
            }
        )
        cls.category_child = cls.env["res.partner.category"].create(
            {
                "name": "Child Category",
                "parent_id": cls.category_parent.id,
            }
        )

    def test_01_default_category_type(self):
        """Test that new categories get the default generic type"""
        category_model = self.env["res.partner.category"]
        default_type = category_model._get_default_category_type()
        self.assertEqual(default_type, "generic")

        new_category = category_model.create(
            {
                "name": "Test Category",
            }
        )
        self.assertEqual(new_category.category_type, "generic")

    def test_02_parent_child_category_type(self):
        """Test that child categories inherit parent's type"""
        # Change parent category type
        self.category_parent.category_type = "generic"
        # Check that child category inherits the type
        self.assertEqual(self.category_child.category_type, "generic")

    def test_03_category_type_constraint(self):
        """Test constraint preventing different types between parent and child"""
        with self.assertRaises(ValidationError):
            self.category_parent.category_type = "generic"
            self.env["res.partner.category"].create(
                {
                    "name": "Invalid Child Category",
                    "parent_id": self.category_parent.id,
                    "category_type": "test",  # Different from parent's 'generic' type
                }
            )

    def test_04_change_parent_category_type(self):
        """Test that changing parent category type updates all children"""
        parent = self.env["res.partner.category"].create({"name": "Parent"})
        child1 = self.env["res.partner.category"].create(
            {"name": "Child 1", "parent_id": parent.id}
        )
        child2 = self.env["res.partner.category"].create(
            {"name": "Child 2", "parent_id": child1.id}
        )

        def extended_selection(self):
            return [("generic", "Generic"), ("test", "Test")]

        original_selection = type(parent)._get_category_type_selection

        try:
            type(parent)._get_category_type_selection = extended_selection
            parent.category_type = "test"
            self.assertEqual(child1.category_type, "test")
            self.assertEqual(child2.category_type, "test")
        finally:
            type(
                parent
            )._get_category_type_selection = (
                original_selection  # Ensure this always runs
            )

    def test_05_compute_category_type(self):
        """Test computation of category type based on parent"""
        # Create standalone category
        standalone = self.env["res.partner.category"].create(
            {
                "name": "Standalone",
            }
        )

        # Verify it gets default type
        self.assertEqual(standalone.category_type, "generic")

        # Set as child of existing category
        standalone.parent_id = self.category_parent.id

        # Verify type is inherited from parent
        self.assertEqual(standalone.category_type, self.category_parent.category_type)

        # Remove parent to test default category assignment
        standalone.parent_id = False

        # Force recompute of category_type
        standalone.invalidate_recordset(["category_type"])
        standalone._compute_category_type()

        # Verify it returns to default category type
        self.assertEqual(standalone.category_type, "generic")

    def test_06_get_category_type_selection(self):
        """Test _get_category_type_selection method"""
        category_model = self.env["res.partner.category"]
        selection = category_model._get_category_type_selection()
        self.assertIn(("generic", "Generic"), selection)
