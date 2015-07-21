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
from openerp.addons.partner_firstname import exceptions


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
    @api.onchange('firstname', 'lastname', 'lastname_second')
    def _onchange_subnames(self):
        """Avoid recursion when the user changes one of these fields.

        This forces to skip the :attr:`~.name` inversion when the user is
        setting it in a not-inverted way.
        """
        self._clean_field('lastname_second', False)
        return super(ResPartner, self)._onchange_subnames()

    @api.one
    @api.constrains("firstname", "lastname", "lastname_second")
    def _check_name(self):
        """Ensure at least one name is set."""
        if not (self.firstname or self.lastname or self.lastname_second):
            raise exceptions.EmptyNamesError(self)

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

    @api.multi
    def _clean_names(self, vals):
        fields = {
            'name': '',
            'firstname': False,
            'lastname': False,
            'lastname_second': False,
        }
        for field, default in fields.iteritems():
            if vals.get(field, None) is not None:
                value = vals.get(field) if vals.get(field) else default
                if value and type(value) in (str, unicode):
                    value = u" ".join(value.split(None))
                    if not value:
                        value = default
                vals[field] = value
        return vals
