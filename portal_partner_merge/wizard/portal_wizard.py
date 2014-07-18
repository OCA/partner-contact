# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (c) 2013 OpenERP S.A. <http://openerp.com>
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
from openerp.tools.translate import _


class wizard_user(orm.TransientModel):
    _inherit = 'portal.wizard.user'

    def get_error_messages(self, cr, uid, ids, context=None):
        error_msg = super(wizard_user, self
                          ).get_error_messages(cr, uid, ids, context=context)
        if error_msg:
            error_msg[-1] = '%s\n%s' % (
                error_msg[-1],
                _("- Merge existing contacts together using the Automatic "
                  "Merge wizard, available in the More menu after selecting "
                  "several contacts in the Customers list"))
        return error_msg
