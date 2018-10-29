# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from odoo import api, fields, models
_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    partner_names_order = fields.Selection(
        string="Partner names order",
        selection="_partner_names_order_selection",
        help="Order to compose partner fullname",
        required=True,
    )
    partner_names_order_changed = fields.Boolean(
        compute="_compute_names_order_changed",
    )

    def _partner_names_order_selection(self):
        return [
            ('last_first', 'Lastname Firstname'),
            ('last_first_comma', 'Lastname, Firstname'),
            ('first_last', 'Firstname Lastname'),
        ]

    @api.multi
    def _partner_names_order_default(self):
        return self.env['res.partner']._names_order_default()

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        partner_names_order = self.env['ir.config_parameter'].sudo().get_param(
            'partner_names_order',
            default=self._partner_names_order_default()
        )
        res.update(partner_names_order=partner_names_order)
        return res

    @api.multi
    @api.depends('partner_names_order')
    def _compute_names_order_changed(self):
        current = self.env['ir.config_parameter'].sudo().get_param(
            'partner_names_order', default=self._partner_names_order_default()
        )
        for record in self:
            record.partner_names_order_changed = bool(
                record.partner_names_order != current
            )

    @api.multi
    @api.onchange('partner_names_order')
    def _onchange_partner_names_order(self):
        self._compute_names_order_changed()

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'partner_names_order', self.partner_names_order
        )

    @api.multi
    def _partners_for_recalculating(self):
        return self.env['res.partner'].search([
            ('is_company', '=', False),
            ('firstname', '!=', False), ('lastname', '!=', False),
        ])

    @api.multi
    def action_recalculate_partners_name(self):
        self.env['ir.config_parameter'].sudo().set_param(
            'partner_names_order', self.partner_names_order
        )
        partners = self._partners_for_recalculating()
        _logger.info("Recalculating names for %d partners.", len(partners))
        partners._compute_name()
        _logger.info("%d partners updated.", len(partners))
        return True
