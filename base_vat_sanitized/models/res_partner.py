# Copyright 2016 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

import re

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sanitized_vat = fields.Char(
        compute='_compute_sanitized_vat', string='Sanitized TIN',
        store=True, readonly=True,
        help='TIN in uppercase without spaces nor special caracters.')

    @classmethod
    def _sanitize_vat(self, vat):
        return vat and re.sub(r'\W+', '', vat).upper() or False

    @api.depends('vat')
    def _compute_sanitized_vat(self):
        for partner in self:
            partner.sanitized_vat = self._sanitize_vat(partner.vat)
