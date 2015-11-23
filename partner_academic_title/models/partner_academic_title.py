# -*- coding: utf-8 -*-
##############################################################################
#
#     This file is part of partner_academic_title,
#     an Odoo module.
#
#     Copyright (c) 2015 ACSONE SA/NV (<http://acsone.eu>)
#
#     partner_academic_title is free software:
#     you can redistribute it and/or modify it under the terms of the GNU
#     Affero General Public License as published by the Free Software
#     Foundation,either version 3 of the License, or (at your option) any
#     later version.
#
#     partner_academic_title is distributed
#     in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
#     even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#     PURPOSE.  See the GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with partner_academic_title.
#     If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields


class PartnerAcademicTitle(models.Model):
    _name = 'partner.academic.title'

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(required=True,
                              help="""defines the order to display titles""")
    active = fields.Boolean(default=True)
