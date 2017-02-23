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

    def _compute_smart_name(self, cr, uid, ids, fields, arg, context=None):
        if context is None:
            context = {}
        else:
            context = context.copy()
        context["preserve_name"] = True

        company = self.pool['res.users'].browse(
            cr, uid, uid, context=context).company_id
        logo_name = (
            company.name_secondary
            if company.has_logo_secondary
            else False
        )

        res = {}
        for rec in self.browse(cr, uid, ids, context=context):
            if logo_name and rec.use_secondary_logo:
                res[rec.id] = ' '.join([rec.name.rstrip(), logo_name])
            else:
                res[rec.id] = rec.name

        return res

    _columns = {
        'use_secondary_logo': fields.boolean('Use Secondary Logo'),
        'smart_name': fields.function(
            _compute_smart_name,
            string="Name", type="char",
        ),
    }

    _defaults = {
        'use_secondary_logo': False
    }

    def read(self, cr, uid, ids, fields, context=None, load="_classic_read"):
        if any((context and context.get("preserve_name"),
                fields and "name" not in fields)):
            # Make sure not to compute smart_name unless necessary.
            # Also: prevent infinite recursion
            return super(IrActionsReportXml, self).read(cr, uid, ids,
                                                        fields=fields,
                                                        context=context,
                                                        load=load)

        if fields and "name" in fields and "smart_name" not in fields:
            fields.append("smart_name")
        res = super(IrActionsReportXml, self).read(cr, uid, ids,
                                                   fields=fields,
                                                   context=context,
                                                   load=load)
        if isinstance(ids, (int, long)):
            target = [res]
        else:
            target = res
        for d in target:
            d["name"] = d["smart_name"]
        return res
