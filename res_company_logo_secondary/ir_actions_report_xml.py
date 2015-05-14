# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
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
from openerp.osv import orm, fields


class IrActionsReportXml(orm.Model):
    _inherit = 'ir.actions.report.xml'

    _columns = {
        'use_secondary_logo': fields.boolean('Use Secondary Logo')
    }

    _defaults = {
        'use_secondary_logo': False
    }

    def write(self, cr, uid, ids, vals, context=None):
        context = context or {}

        if 'use_secondary_logo' in vals:
            assert len(ids) == 1, "you can only modify the report logo one at a time"
            logo_name = self.pool['res.users'].browse(
                cr, uid, uid, context=context).company_id.name_secondary
            name = vals.get('name', False) or self.browse(
                cr, uid, ids[0], context=context).name
            if vals['use_secondary_logo']:
                vals['name'] = ' '.join([name.strip(logo_name), logo_name])
            else:
                vals['name'] = name.strip(logo_name)

        return super(IrActionsReportXml, self).write(
            cr, uid, ids, vals, context=context)
