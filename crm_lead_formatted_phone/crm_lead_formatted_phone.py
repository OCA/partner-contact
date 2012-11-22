# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
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

import re
from osv import fields, osv

class crm_lead_formatted_phone(osv.osv):
    _inherit = 'crm.lead'
    
    def on_change_phone(self, cr, uid, ids, field_name, phone, country_id=False):
        result = phone
        if phone:
            digits = [c for c in phone if c.isdigit()]
            if len(digits) >= 10:
                result = u"(%s) %s-%s" % ("".join(digits[0:3]), "".join(digits[3:6]), 
                        "".join(digits[6:10]))
                if len(digits) > 10:
                    result += " x %s" % "".join(digits[10:])
        return { 'value': { field_name: result } }

crm_lead_formatted_phone()
