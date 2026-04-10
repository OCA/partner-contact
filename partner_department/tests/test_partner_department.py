# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestPartnerDepartment(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Partner = cls.env["res.partner"]
        cls.company = cls.Partner.create({"name": "Acme Corp", "is_company": True})
        cls.department = cls.Partner.create(
            {"name": "Engineering", "type": "department", "parent_id": cls.company.id}
        )
        cls.contact1 = cls.Partner.create(
            {
                "name": "John Doe",
                "parent_id": cls.company.id,
                "department_id": cls.department.id,
            }
        )
        cls.contact2 = cls.Partner.create(
            {
                "name": "Jane Smith",
                "parent_id": cls.company.id,
                "department_id": cls.department.id,
            }
        )

    def test_department_type(self):
        """Department partner has type='department'"""
        self.assertEqual(self.department.type, "department")

    def test_department_is_partner(self):
        """Department is a real res.partner, not a company, selectable anywhere"""
        self.assertFalse(self.department.is_company)
        found = self.Partner.search([("id", "=", self.department.id)])
        self.assertEqual(len(found), 1)

    def test_contact_department_id(self):
        """Contacts have the correct department_id assigned"""
        self.assertEqual(self.contact1.department_id, self.department)
        self.assertEqual(self.contact2.department_id, self.department)

    def test_department_member_ids(self):
        """department_member_ids returns all contacts assigned to the department"""
        self.assertIn(self.contact1, self.department.department_member_ids)
        self.assertIn(self.contact2, self.department.department_member_ids)

    def test_search_by_department_type(self):
        """Can search partners filtered by type='department'"""
        departments = self.Partner.search([("type", "=", "department")])
        self.assertIn(self.department, departments)

    def test_search_contacts_by_department(self):
        """Can search contacts filtered by department_id"""
        contacts = self.Partner.search([("department_id", "=", self.department.id)])
        self.assertIn(self.contact1, contacts)
        self.assertIn(self.contact2, contacts)

    def test_department_not_in_own_members(self):
        """A department partner does not appear in its own member list"""
        self.assertNotIn(self.department, self.department.department_member_ids)

    def test_unassign_department(self):
        """Removing department_id from a contact updates the member list"""
        self.contact1.write({"department_id": False})
        self.assertFalse(self.contact1.department_id)
        self.assertNotIn(self.contact1, self.department.department_member_ids)

    def test_multiple_departments(self):
        """Two departments of the same company have independent member lists"""
        dept_sales = self.Partner.create(
            {"name": "Sales", "type": "department", "parent_id": self.company.id}
        )
        contact = self.Partner.create(
            {
                "name": "Alice",
                "parent_id": self.company.id,
                "department_id": dept_sales.id,
            }
        )
        self.assertIn(contact, dept_sales.department_member_ids)
        self.assertNotIn(contact, self.department.department_member_ids)
