# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Savoir-faire Linux
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
from openerp.tools.translate import _


class res_partner(orm.Model):
    _inherit = 'res.partner'
    _columns = {
        'passport_ids': fields.one2many('res.passport', 'partner_id', 'Passport'),
    }

    def action_add_passport_form_view(self, cr, uid, ids, context=None):
        """Call action, if there is a contact, put it in the name."""
        ir_model_data = self.pool.get('ir.model.data')
        contacts = self.browse(cr, uid, ids, context=context)
        contact_name = ('%s : %s ' % (contacts[0].full_name, _('New Passport')) if len(contacts) == 1 else False)
        name = contact_name or _('New Passport')
        try:
            compose_form_id = ir_model_data.get_object_reference(cr, uid, 'passport_partner', 'add_passport_form_view')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict(context)
        ctx.update({
            'default_res_id': ids[0],
            'default_partner_id': ids[0],
        })
        return {
            'name': name,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'res.passport',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
