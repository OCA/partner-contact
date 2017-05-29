# -*- coding: utf-8 -*-
# © 2016 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).
from odoo.tests import common
from odoo.exceptions import ValidationError


class TestRecursion(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestRecursion, cls).setUpClass()
        cls.department_obj = cls.env['res.partner.department']

        # Instances
        cls.dpt1 = cls.department_obj.create(vals=dict(name='Dpt. 1'))
        cls.dpt2 = cls.department_obj.create(
            vals=dict(
                name='Dpt. 2',
                parent_id=cls.dpt1.id
            ))

    def test_recursion(self):
        """ Testing recursion """
        self.dpt3 = self.department_obj.create(vals=dict(
            name='Dpt. 3',
            parent_id=self.dpt2.id
        ))
        # Creating a parent's child department using dpt1.
        with self.assertRaises(ValidationError):
            self.dpt1.write(vals={'parent_id': self.dpt3.id})
