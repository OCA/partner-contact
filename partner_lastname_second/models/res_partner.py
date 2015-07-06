# -*- coding: utf-8 -*-
# Python source code encoding : https://www.python.org/dev/peps/pep-0263/
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2015 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Antonio Espinosa <antonioea@antiun.com>
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


class ResPartner(models.Model):
    _inherit = 'res.partner'

    lastname_second = fields.Char(string='Second lastname')

    @api.one
    @api.depends('firstname', 'lastname', 'lastname_second', 'company_id')
    def _compute_name(self):
        names = (self.lastname, self.lastname_second, self.firstname)
        if self.company_id.names_order == 'first_last':
            names = (self.firstname, self.lastname, self.lastname_second)
        self.name = u' '.join(filter(None, names))

    @api.one
    def _inverse_name(self):
        super(ResPartner, self)._inverse_name()
        lastname_second = False
        if not self.is_company and self.lastname:
            parts = self.lastname.split(' ')
            if len(parts) > 1:
                lastname_second = parts[-1]
                self.lastname = u' '.join(parts[:-1])
        self.lastname_second = lastname_second
