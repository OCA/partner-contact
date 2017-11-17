# -*- coding: utf-8 -*-
# Copyright 2016 Nicolas Bessi, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCountryState(models.Model):

    _inherit = 'res.country'

    geonames_state_name_column = fields.Integer(
        u'Geoname State Name Column',
        default=3
    )
    geonames_state_code_column = fields.Integer(
        u'Geoname State Name Code',
        default=4
    )
