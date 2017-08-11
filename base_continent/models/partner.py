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


class Partner(models.Model):
    _inherit = 'res.partner'

    continent_id = fields.Many2one(
        comodel_name='res.continent',
        string='Continent',
        readonly=True,
        store=True,
        related='country_id.continent_id',
    )
