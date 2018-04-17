# -*- coding: utf-8 -*-
# Copyright 2017 Grant Thornton Spain - Ismael Calvo <ismael.calvo@es.gt.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.constrains('vat')
    def _check_vat_unique(self):
        for record in self:
            if record.parent_id:
                continue
            results = self.env['res.partner'].search([
                ('parent_id', '=', False),
                ('vat', '=', record.vat),
                ('id', '!=', record.id)
            ])
            if results:
                raise ValidationError(_(
                    "The VAT %s already exists in another "
                    "partner.") % record.vat)
