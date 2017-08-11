# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Romain Deheele
#    Copyright 2014 Camptocamp SA
#
#    Author: Quentin Theuret
#    Copyright 2017 SenseFly, Amaris
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models
from odoo import fields


class Continent(models.Model):
    _name = 'res.continent'
    _description = 'Continent'
    _order = 'name'

    name = fields.Char(
        string='Continent Name',
        size=64,
        help="""The full name of the continent.""",
        required=True,
        translate=True,
    )
    code = fields.Char(
        string='Continent Code',
        size=2,
        required=True,
    )
    countries = fields.One2many(
        comodel_name='res.country',
        inverse_name='continent_id',
        string='Countries',
        readonly=True,
    )

