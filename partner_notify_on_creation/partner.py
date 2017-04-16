##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Savoir-faire Linux
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

from openerp.osv import fields, orm


class res_partner(orm.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    def create(self, cr, uid, data, context=None):
        partner_id = super(res_partner, self).create(
            cr, uid, data, context=context
        )
        # Send email when creating a new partner
        tmpl_obj = self.pool.get('email.template')
        tmpl_ids = tmpl_obj.search(
            cr, uid, [('name', '=', 'Partner Notify on Creation')])
        if tmpl_ids:
            context['default_composition_mode'] = 'mass_mail'
        for partner in self.browse(cr, uid, [partner_id], context=context):
            self.pool.get('email.template').send_mail(
                cr, uid, tmpl_ids[0], partner.id, True, context=context)
        return partner_id
