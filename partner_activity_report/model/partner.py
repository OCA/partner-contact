# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Vincent Renaville, Damien Crier
#    Copyright 2014-2015 Camptocamp SA
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

from openerp import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def get_partner_crm_informations(self):
        crm_obj = self.env['crm.lead']
        lead_partners = crm_obj.search([('partner_id', '=', self.id)])
        return lead_partners

    @api.multi
    def get_partner_invoice_informations(self):
        account_invoice_obj = self.env['account.invoice']
        account_invoices = account_invoice_obj.search(
            [('partner_id', '=', self.id)]
            )
        return account_invoices

    @api.multi
    def get_partner_sales_informations(self):
        sales_obj = self.env['sale.order']
        sales = sales_obj.search([('partner_id', '=', self.id)])
        return sales

    @api.multi
    def get_partner_deliveries_informations(self):
        stock_location_obj = self.env['stock.location']
        stock_moves_obj = self.env['stock.move']
        locations = stock_location_obj.search([('usage', '=', 'customer')])
        moves = stock_moves_obj.search(
            [('partner_id', '=', self.id),
             ('location_dest_id', 'in', locations.ids),
             ('state', '=', 'done'),
             ]
            )
        return moves
