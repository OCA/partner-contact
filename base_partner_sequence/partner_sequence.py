# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2013 initOS GmbH & Co. KG (<http://www.initos.com>).
#    Author Thomas Rehn <thomas.rehn at initos.com>
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

from osv import osv, fields
import logging
_logger = logging.getLogger(__name__)

class partner_sequence(osv.osv):
    _inherit = 'res.partner'
    def create(self, cr, uid, vals, context={}):
        # only assign a 'ref' if it is not a child object
        #  (such as a shipping/invoice address)
        if vals.get('parent_id', 0) > 0:
            vals['ref'] = self.pool.get('ir.sequence').get(cr, uid, 'res.partner')
        res = super(partner_sequence, self).create(cr, uid, vals, context)
        return res
    _columns = {
        'ref': fields.char('Code', size=64, readonly=True),
    }
partner_sequence()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

