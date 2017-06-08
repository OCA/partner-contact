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

from openerp import models, fields, api
from openerp.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = 'res.company'

    logo_ids = fields.One2many('res.company.logo', 'company_id', 'Logos')

    @api.one
    @api.constrains('logo_ids')
    def _check_one_default_logo(self):
        if self.logo_ids:
            default_logo = self.logo_ids.filtered('is_default')
            if len(default_logo) != 1:
                raise ValidationError(
                    "You must define one and only one logo as default.")
