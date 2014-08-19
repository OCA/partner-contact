# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010 Camptocamp SA (http://www.camptocamp.com)
# All Right Reserved
#
# Author : Nicolas Bessi (Camptocamp),
# Thanks to Laurent Lauden for his code adaptation
# Active directory Donor: M. Benadiba (Informatique Assistances.fr)
# Contribution : Joel Grand-Guillaume
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from openerp.osv import orm


class LdapPartner(orm.Model):
    """Ensure that when deleting a partner unlink function is called on all
    related addresses"""
    _inherit = 'res.partner'

    def unlink(self, cr, uid, ids, context=None):
        context = context or {}
        addr_obj = self.pool.get('res.partner.address')
        if not isinstance(ids, list):
            ids = [ids]
        addr_ids = addr_obj.search(cr, uid, [('partner_id', 'in', ids)])
        addr_obj.unlink(cr, uid, addr_ids, context=context)
        return super(LdapPartner, self).unlink(cr, uid, ids, context=context)
