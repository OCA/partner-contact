# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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


class partner_print_activity(models.TransientModel):
    _name = 'partner.print.activity'
    _description = 'Partner printing activity'

    @api.model
    def _get_partner_ids(self):
        context = self.env.context
        if context.get('active_model') != 'res.partner':
            return False
        return context.get('active_ids', False)

    partner_information = fields.Boolean(string='Print partner address',
                                  default=True)
    partner_address_information = fields.Boolean(string='Print partner contacts',
                                  default=True)
    partner_crm_renouvellement = fields.Boolean(string='Print partner recent CRM case',
                                  default=True)
    partner_invoice = fields.Boolean(string='Print partner recent invoices',
                                  default=True)
    partner_sales_order = fields.Boolean(string='Print partner recent sale orders',
                                  default=True)
    partner_delivery_lines = fields.Boolean(string='Print partner recent delivery lines',
                                  default=True)

    partner_ids = fields.Many2many('res.partner',
                                string='Partner ids',
                                default=_get_partner_ids)



    @api.multi
    def print_report(self):
        self.ensure_one()
        comm_obj = self.env['partner.print.activity']
        partner_obj = self.env['res.partner']
        if not self.partner_ids:
            raise api.Warning(_('No partner Select'))
        report_name = 'partner_activity_report.report_partner_activity_qweb'
        report_obj = self.env['report'].with_context(active_ids=self.partner_ids.ids)
        return report_obj.get_action(self, report_name)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
