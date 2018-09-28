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

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _get_separator(self):
        return ', '

    @api.depends('academic_title_ids', 'academic_title_ids.sequence')
    @api.one
    def _get_academic_title_display(self):
        display_title = ""
        separator = self._get_separator()
        title_ids = self.academic_title_ids.sorted(lambda r: r.sequence)
        for title in title_ids:
            if display_title:
                display_title = "%s%s%s" % (display_title, separator,
                                            title.name)
            else:
                display_title = "%s" % (title.name)
        self.academic_title_display = display_title

    academic_title_ids = fields.Many2many(
        comodel_name='partner.academic.title',
        relation='partner_academic_title_ref', column1='partner_id',
        column2='academic_title_id', string='Academic Titles')
    academic_title_display = fields.Char(compute='_get_academic_title_display',
                                         string='Academic Titles', store=True)
