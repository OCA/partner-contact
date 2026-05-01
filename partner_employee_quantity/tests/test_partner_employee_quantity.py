# Copyright 2015 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2015 Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.base.tests.common import BaseCommon


class TestResPartnerEmployeeQuantityRange(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.employee_range1 = cls.env["res.partner.employee_quantity_range"].create(
            {"name": "1-10 Employees"}
        )
        cls.employee_range2 = cls.env["res.partner.employee_quantity_range"].create(
            {"name": "11-50 Employees"}
        )

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "employee_quantity": 15,
                "employee_quantity_range_id": cls.employee_range2.id,
            }
        )

    def test_employee_quantity_range(self):
        """Test that the employee quantity range is correctly assigned"""
        self.assertEqual(self.partner.employee_quantity, 15)
        self.assertEqual(self.partner.employee_quantity_range_id, self.employee_range2)

    def test_update_employee_quantity_range(self):
        """Test updating the employee quantity range"""
        self.partner.write(
            {
                "employee_quantity": 5,
                "employee_quantity_range_id": self.employee_range1.id,
            }
        )
        self.assertEqual(self.partner.employee_quantity, 5)
        self.assertEqual(self.partner.employee_quantity_range_id, self.employee_range1)
