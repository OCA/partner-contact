# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    logo_ids = fields.Many2many(
        'res.company.logo', string='Report Logos')

    @api.one
    @api.constrains('logo_ids')
    def _check_one_logo_per_company(self):
        logos = self.logo_ids
        if len({logo.company_id for logo in logos}) < len(logos):
            raise ValidationError(_(
                "You cannot select more than one logo per company for one "
                "partner!"))

    @api.multi
    def get_company_logo(self, company):
        self.ensure_one()
        logo = self.logo_ids.filtered(lambda l: l.company_id == company)
        if not logo:
            logo = company.logo_ids.filtered('is_default')
        return logo.image
