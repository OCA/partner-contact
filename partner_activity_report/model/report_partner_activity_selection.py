# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright 2015 Camptocamp SA
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

from operator import attrgetter
from openerp import models


class PartnerActivityReport(models.AbstractModel):
    _name = 'report.partner_activity_report.report_partner_activity_qweb'

    def render_html(self, cr, uid, ids, data=None, context=None):
        report_obj = self.pool['report']
        partner_activity_obj = self.pool['partner.print.activity']
        report_name = 'partner_activity_report.report_partner_activity_qweb'
        report = report_obj._get_report_from_name(cr, uid, report_name)
        wizard_selection = partner_activity_obj.browse(cr, uid, ids, context=context)[0]
        
        docargs = {
            'doc_ids': wizard_selection.partner_ids.ids,
            'doc_model': report.model,
            'docs': wizard_selection.partner_ids,
            'option_selected': wizard_selection,
            'get_partner_crm_informations': self.get_partner_crm_informations,
            'get_partner_invoice_informations': self.get_partner_invoice_informations,
            'get_partner_sales_informations': self.get_partner_sales_informations,
            'get_partner_deliveries_informations': self.get_partner_delivery_informations,
        }
        html = report_obj.render(cr, uid, ids, report_name,
                                 docargs, context=context)
        return html

    def get_partner_crm_informations(self, partner):
        crm_obj = self.pool['crm.lead']
        lead_partner_ids = crm_obj.search(['partner_id','=',partner.id])
        return crm_obj.browse(lead_partner_ids)

    def get_partner_invoice_informations(self, partner):
        account_invoice_obj = self.pool['account.invoice']
        account_invoice_ids = account_invoice_obj.search(['partner_id','=',partner.id])
        return account_invoice_obj.browse(account_invoice_ids)

    def get_partner_sales_informations(self, partner):
        sales_obj = self.pool['sales.order']
        sale_ids = sales_obj.search(['partner_id','=',partner.id])
        return sales_obj.browse(sale_ids)

    def get_partner_delivery_informations(self, partner):
        stock_location_obj = self.pool['stock.location']
        stock_moves_obj = self.pool['stock.moves']
        location_ids = stock_location_obj.search([('usage','=','customer')])
        move_ids = stock_moves_obj.search(['partner_id','=',partner.id],
                                          ['location_dest_id','in',location_ids],
                                          ['state','=','done'])
        return stock_moves_obj.browse(move_ids)
