# -*- coding: utf-8 -*-
# © 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _


class PartnerRiskExceededWiz(models.TransientModel):
    _name = 'partner.risk.exceeded.wiz'

    partner_id = fields.Many2one(
        comodel_name='res.partner', readonly=True, string='Customer')
    exception_msg = fields.Text(readonly=True)
    origin_reference = fields.Reference(
        lambda self: [
            (m.model, m.name) for m in self.env['ir.model'].search([])],
        string='Object')
    continue_method = fields.Char()

    @api.multi
    def action_show(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Partner risk exceeded'),
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }

    @api.multi
    def button_continue(self):
        self.ensure_one()
        return getattr(self.origin_reference.with_context(
            bypass_risk=True), self.continue_method)()
