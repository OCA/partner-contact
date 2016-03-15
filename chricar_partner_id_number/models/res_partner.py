# -*- coding: utf-8 -*-
# Python source code encoding : https://www.python.org/dev/peps/pep-0263/
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL
#                            http://tiny.be
#    Copyright (C) 2010-2012 ChriCar Beteiligungs- und Beratungs- GmbH
#                            http://www.camptocamp.at
#    Copyright (C) 2015 Antiun Ingenieria, SL (Madrid, Spain)
#                       http://www.antiun.com
#                       Antonio Espinosa <antonioea@antiun.com>
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

from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    id_numbers = fields.One2many(
        comodel_name='res.partner.id_number', inverse_name='partner_id',
        string="Identification Numbers")
