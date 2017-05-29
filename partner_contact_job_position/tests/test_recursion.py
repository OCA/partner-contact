# -*- coding: utf-8 -*-
# © 2016 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).
from openerp.tests import common
from openerp.exceptions import ValidationError


class TestRecursion(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestRecursion, cls).setUpClass()
        cls.job_obj = cls.env['res.partner.job_position']

        # Instances
        cls.grand_parent = cls.job_obj.create(vals=dict(name='Grand parent'))
        cls.parent = cls.job_obj.create(vals=dict(
            name='Parent',
            parent_id=cls.grand_parent.id
        ))

    def test_recursion(self):
        """ Testing recursion """
        self.child = self.job_obj.create(vals=dict(
            name='Grand parent',
            parent_id=self.parent.id
        ))
        # Creating a parent's child using grand-parent
        with self.assertRaises(ValidationError):
            self.grand_parent.write(vals={'parent_id': self.child.id})
