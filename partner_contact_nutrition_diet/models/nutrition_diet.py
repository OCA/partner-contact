# -*- coding: utf-8 -*-
# Copyright 2016 Ursa Information Systems <http://ursainfosystems.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import fields, models


class NutritionDiet(models.Model):
    _name = 'nutrition.diet'

    name = fields.Char("Name")
