# Copyright 2015-2017 ACSONE SA/NV (<https://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _get_separator(self):
        return ', '

    @api.multi
    @api.depends('academic_title_ids', 'academic_title_ids.sequence')
    def _compute_academic_title_display(self):
        for this in self:
            display_title = ""
            separator = this._get_separator()
            title_ids = this.academic_title_ids.sorted(lambda r: r.sequence)
            if title_ids:
                display_title = separator.join(
                    [title.name for title in title_ids])
            this.academic_title_display = display_title

    academic_title_ids = fields.Many2many(
        string='Academic Titles',
        comodel_name='partner.academic.title',
        relation='partner_academic_title_ref',
        column1='partner_id',
        column2='academic_title_id'
    )
    academic_title_display = fields.Char(
        string='Academic Titles',
        compute='_compute_academic_title_display',
        store=True
    )
