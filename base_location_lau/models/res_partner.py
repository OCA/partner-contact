# -*- coding: utf-8 -*-
# © 2016 Daniel Reis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    lau1_id = fields.Many2one(
        'res.partner.lau',
        'Local Admin. Unit 1',
        domain=[('level', '=', 1)])
    lau2_id = fields.Many2one(
        'res.partner.lau',
        'Local Admin. Unit 2',
        domain=[('level', '=', 2)])

    @api.multi
    @api.onchange('lau1_id')
    def _onchange_lau1(self):
        for p in self:
            if p.lau2_id and p.lau2_id.parent_id != p.lau1_id:
                p.lau2_id = None
