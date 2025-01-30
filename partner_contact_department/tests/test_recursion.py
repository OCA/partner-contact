# © 2016 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestRecursion(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.department_obj = cls.env["res.partner.department"]

        # Instances
        cls.dpt1 = cls.department_obj.create({"name": "Dpt. 1"})
        cls.dpt2 = cls.department_obj.create(
            {"name": "Dep. 2", "parent_id": cls.dpt1.id}
        )

    def test_recursion(self):
        """Testing recursion"""
        self.dpt3 = self.department_obj.create(
            {"name": "Dep. 3", "parent_id": self.dpt2.id}
        )
        # Creating a parent's child department using dpt1.
        with self.assertRaises(UserError):
            self.dpt1.write({"parent_id": self.dpt3.id})

    def test_create_department(self):
        """Test creating a new department"""
        new_department = self.department_obj.create({"name": "New Department"})
        self.assertTrue(new_department, "New department should be created")

    def test_update_department(self):
        """Test updating an existing department"""
        self.dpt1.write({"name": "Updated Department"})
        self.assertEqual(
            self.dpt1.name, "Updated Department", "Department name should be updated"
        )

    def test_delete_department(self):
        """Test deleting a department"""
        department_to_delete = self.department_obj.create(
            {"name": "Department to Delete"}
        )
        department_to_delete.unlink()
        self.assertFalse(department_to_delete.exists(), "Department should be deleted")
