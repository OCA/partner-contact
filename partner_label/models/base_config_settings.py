# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class BaseConfigSettings(models.TransientModel):
    _inherit = 'base.config.settings'

    partner_labels_width = fields.Float(
        related='company_id.partner_labels_width', required=True,
    )
    partner_labels_height = fields.Float(
        related='company_id.partner_labels_height', required=True,
    )
    partner_labels_padding = fields.Float(
        related='company_id.partner_labels_padding', required=True,
    )
    partner_labels_margin = fields.Float(
        related='company_id.partner_labels_margin', required=True,
    )
    partner_labels_paperformat_id = fields.Many2one(
        'report.paperformat', string='Paperformat', required=True,
        default=lambda self: self.env.ref(
            'partner_label.report_res_partner_label'
        ).paperformat_id,
        compute='_compute_partner_labels_paperformat_id',
        inverse='_inverse_partner_labels_paperformat_id',
    )

    @api.multi
    def _compute_partner_labels_paperformat_id(self):
        for this in self:
            this.partner_labels_paperformat_id = self.env.ref(
                'partner_label.report_res_partner_label'
            ).paperformat_id

    @api.multi
    def _inverse_partner_labels_paperformat_id(self):
        for this in self:
            self.env.ref(
                'partner_label.report_res_partner_label'
            ).paperformat_id = this.partner_labels_paperformat_id

    @api.multi
    def action_partner_labels_preview(self):
        return self.env['report'].get_action(
            self.env['res.partner'].search([], limit=100),
            'partner_label.view_res_partner_label',
        )
