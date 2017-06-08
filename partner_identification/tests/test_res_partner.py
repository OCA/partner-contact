# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.tests import common
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    social_security = fields.Char(
        compute=lambda s: s._compute_identification(
            'social_security', 'SSN',
        ),
        inverse=lambda s: s._inverse_identification(
            'social_security', 'SSN',
        ),
        search=lambda s, *a: s._search_identification(
            'SSN', *a
        ),
    )


class TestResPartner(common.SavepointCase):

    @classmethod
    def _init_test_model(cls, model_cls):
        """ Build a model from model_cls in order to test abstract models.
        Note that this does not actually create a table in the database, so
        there may be some unidentified edge cases.
        Args:
            model_cls (openerp.models.BaseModel): Class of model to initialize
        Returns:
            model_cls: Instance
        """
        registry = cls.env.registry
        cr = cls.env.cr
        inst = model_cls._build_model(registry, cr)
        model = cls.env[model_cls._inherit].with_context(todo=[])
        model._prepare_setup()
        model._setup_base(partial=False)
        model._setup_fields(partial=False)
        model._setup_complete()
        model._auto_init()
        model.init()
        model._auto_end()
        return inst

    @classmethod
    def setUpClass(cls):
        super(TestResPartner, cls).setUpClass()
        cls.env.registry.enter_test_mode()
        cls._init_test_model(ResPartner)

    def setUp(self):
        super(TestResPartner, self).setUp()
        bad_cat = self.env['res.partner.id_category'].create({
            'code': 'another_code',
            'name': 'another_name',
        })
        self.env['res.partner.id_number'].create({
            'name': 'Bad ID',
            'category_id': bad_cat.id,
            'partner_id': self.env.user.partner_id.id,
        })
        self.partner_id_category = self.env['res.partner.id_category'].create({
            'code': 'id_code',
            'name': 'id_name',
        })
        self.partner = self.env.user.partner_id
        self.partner_id = self.env['res.partner.id_number'].create({
            'name': 'Good ID',
            'category_id': self.partner_id_category.id,
            'partner_id': self.partner.id,
        })

    def test_compute_identification(self):
        """ It should set the proper field to the proper ID name. """
        self.partner._compute_identification('name',  'id_code')
        self.assertEqual(self.partner.name, self.partner_id.name)

    def test_inverse_identification_saves(self):
        """ It should set the ID name to the proper field value. """
        self.partner._inverse_identification('name',  'id_code')
        self.assertEqual(self.partner_id.name, self.partner.name)

    def test_inverse_identification_creates_new_category(self):
        """ It should create a new category of the type if non-existent. """
        self.partner._inverse_identification('name', 'new_code_type')
        category = self.env['res.partner.id_category'].search([
            ('code', '=', 'new_code_type'),
        ])
        self.assertTrue(category)

    def test_inverse_identification_creates_new_id(self):
        """ It should create a new ID of the type if non-existent. """
        category = self.env['res.partner.id_category'].create({
            'code': 'new_code_type',
            'name': 'new_code_type',
        })
        self.partner._inverse_identification('name', 'new_code_type')
        identification = self.env['res.partner.id_number'].search([
            ('category_id', '=', category.id),
            ('partner_id', '=', self.partner.id),
        ])
        self.assertEqual(identification.name, self.partner.name)

    def test_inverse_identification_multi_exception(self):
        """ It should not allow a write when multiple IDs of same type. """
        self.env['res.partner.id_number'].create({
            'name': 'Another ID',
            'category_id': self.partner_id_category.id,
            'partner_id': self.partner.id,
        })
        with self.assertRaises(ValidationError):
            self.partner._inverse_identification('name', 'id_code')

    def test_search_identification(self):
        """ It should return the right record when searched by ID. """
        self.partner.social_security = 'Test'
        partner = self.env['res.partner'].search([
            ('social_security', '=', 'Test'),
        ])
        self.assertEqual(partner, self.partner)
