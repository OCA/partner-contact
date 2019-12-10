# Copyright (C) 2019 Compassion CH (http://www.compassion.ch)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import datetime
from odoo import models, fields, api
from odoo.tools.safe_eval import safe_eval


class ResPartnerCategory(models.Model):
    _inherit = "res.partner.category"

    condition_id = fields.Many2one('ir.filters', string="Condition")
    smart = fields.Boolean()
    partner_field = fields.Char(
        default='partner_id',
        help='Relational field used on the filter object to find the partners.'
    )
    partner_ids = fields.Many2many("res.partner",
                                   relation='res_partner_res_partner_'
                                            'category_rel',
                                   column1='category_id',
                                   column2='partner_id')

    number_tags = fields.Integer(compute='_compute_number_tags', stored=True)

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record.update_partner_tags()
        return record

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        if 'condition_id' in vals or 'model' in vals:
            self.update_partner_tags()
        return res

    @api.constrains('condition_id')
    def check_condition(self):
        for me in self:
            if me.condition_id.model_id != 'res.partner':
                model_link = self.env[me.condition_id.model_id]
                if 'partner_id' not in model_link:
                    raise ValueError(
                        "The chosen model has no partner_id field")

    @api.multi
    def update_partner_tags(self):
        for tagger in self.filtered('smart'):
            domain = safe_eval(tagger.condition_id.domain,
                               locals_dict={'datetime': datetime},
                               locals_builtins=True)
            model = tagger.condition_id.model_id
            matching_records = self.env[model].search(domain)
            if matching_records:
                if model == 'res.partner':
                    partner_ids = matching_records.ids
                else:
                    partner_ids = matching_records.mapped(
                        tagger.partner_field).ids
                tagger.write({'partner_ids': [(6, 0, partner_ids)]})
        return True

    @api.model
    def update_all_smart_tags(self):
        return self.search([('smart', '=', True)]).update_partner_tags()

    @api.depends('partner_ids')
    def _compute_number_tags(self):
        for category in self:
            category.number_tags = len(category.partner_ids)

    @api.multi
    def open_tags(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "res.partner",
            "view_type": "form",
            "view_mode": "list,form",
            "name": "Partners",
            "domain": [["id", "in", self.partner_ids.ids]]
        }
