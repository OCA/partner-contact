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


class PartnerActivityReport(models.AbstractModel):
    _name = 'report.partner_activity_report.report_partner_activity_qweb'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        partner_activity_obj = self.env['partner.print.activity']
        report_name = 'partner_activity_report.report_partner_activity_qweb'
        report = report_obj._get_report_from_name(report_name)
        wizard_selection = partner_activity_obj.browse(self.ids)[0]

        docargs = {
            'doc_ids': wizard_selection.ids,
            'doc_model': report.model,
            'docs': wizard_selection,
            'option_selected': wizard_selection,
        }
        html = report_obj.render(report_name,
                                 docargs)
        return html
