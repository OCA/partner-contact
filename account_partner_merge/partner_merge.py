# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Yannick Vaucher
#    Copyright 2013 Camptocamp SA
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
from openerp.osv import orm


class MergePartnerAutomatic(orm.TransientModel):
    _inherit = 'base.partner.merge.automatic.wizard'

    def _update_values(self, cr, uid, src_partners, dst_partner, context=None):
        """Make sure we don't forget to update the stored value of
        invoice field commercial_partner_id
        """
        super(MergePartnerAutomatic, self)._update_values(
            cr, uid, src_partners, dst_partner, context=context
        )

        invoice_obj = self.pool.get('account.invoice')
        invoice_ids = invoice_obj.search(
            cr, uid, [('partner_id', '=', dst_partner.id)], context=context
        )
        # call write to refresh stored value
        invoice_obj.write(cr, uid, invoice_ids, {}, context=context)
