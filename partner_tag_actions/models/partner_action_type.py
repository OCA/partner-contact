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


class PartnerActionType(models.Model):
    _name = 'partner.action.type'
    _description = 'Partner Action Type'
    _order = 'priority'

    name = fields.Char('Name', translate=True, required=True)
    priority = fields.Integer('Priority', required=True, default=0)
    is_active = fields.Boolean('Active', default=True)

    add_tag = fields.Many2one('res.partner.category', required=False,
                              string='Add Tag')
    remove_tag = fields.Many2one('res.partner.category', required=False,
                                 string='Remove Tag')

    @api.model
    def get_default(self):
        return self.search([('is_active', '=', True)], limit=1).id
