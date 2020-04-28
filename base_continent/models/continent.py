# -*- coding: utf-8 -*-
# © 2014-2016 Camptocamp SA (Author: Romain Deheele)
# © 2017 senseFly, Amaris (Author: Quentin Theuret)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from odoo import fields


class Continent(models.Model):
    _name = 'res.continent'
    _description = 'Continent'
    _order = 'name'

    name = fields.Char(
        string='Continent Name',
        help='The full name of the continent.',
        required=True,
        translate=True,
    )
    code = fields.Char(
        string='Continent Code',
        size=2,
        required=True,
    )
    country_ids = fields.One2many(
        comodel_name='res.country',
        inverse_name='continent_id',
        string="Countries",
    )
