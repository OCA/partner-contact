######################################################################################################
#
# Copyright (C) B.H.C. sprl - All Rights Reserved, http://www.bhc.be
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied,
# including but not limited to the implied warranties
# of merchantability and/or fitness for a particular purpose
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
# -*- coding: utf-8 -*-
import datetime
from lxml import etree
import math
import pytz
import urlparse

import openerp
from openerp import tools, api 
from openerp.osv import osv, fields
from openerp.osv.expression import get_unaccent_wrapper
from openerp.tools.translate import _

class res_partner(osv.Model):
    _inherit = "res.partner"
    
    def _check_categ(self, cr, uid, ids, name, args, context):
        res={}
        bl=self.pool.get('res.partner.category').search(cr,uid,[('blacklist','=',True)])
        if bl and len(ids)==1:
            for i in self.browse(cr,uid,ids):
                for j in i.category_id:
                    if j.blacklist==True:
                        res[i.id]=1
                    else:
                        res[i.id]=0
        return res
    
    _columns = {
        'blacklist': fields.function(_check_categ, method=True, string=_('Blacklist'), type='boolean', store=True ),
    }
res_partner()

class category(osv.Model):
    _inherit = "res.partner.category"
    _columns = {
        'blacklist': fields.boolean(_('Blacklist')),
    }
category()