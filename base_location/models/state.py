# -*- coding: utf-8 -*-
# Copyright 2016 Nicolas Bessi, Copyright Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import models, fields


class ResCountryState(models.Model):

    _inherit = 'res.country.state'

    better_zip_ids = fields.One2many('res.better.zip', 'state_id', 'Cities')
