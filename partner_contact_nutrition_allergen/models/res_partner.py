# -*- coding: utf-8 -*-
# Copyright 2016 Ursa Information Systems <http://ursainfosystems.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    nutrition_allergen_ids = fields.Many2many(comodel_name='product.product',
                                              string='Allergens',
                                              domain="[('type', '=',"
                                                     " 'stockable')]")
