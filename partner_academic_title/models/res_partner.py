# -*- coding: utf-8 -*-
# Copyright 2015-2017 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


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
        string='Academic Titles',
        comodel_name='partner.academic.title',
        relation='partner_academic_title_ref',
        column1='partner_id',
        column2='academic_title_id'
    )
    academic_title_display = fields.Char(
        string='Academic Titles',
        compute='_get_academic_title_display',
        store=True
    )
