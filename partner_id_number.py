##############################################
#
# ChriCar Beteiligungs- und Beratungs- GmbH
# Copyright (C) ChriCar Beteiligungs- und Beratungs- GmbH
# all rights reserved
# created 2008-07-05
#
###############################################
import time
from osv import fields,osv
import pooler

class res_partner_id_category(osv.osv):
     _name = "res.partner.id_category"
     _columns = {
       'code'               : fields.char    ('Code', size=16, required=True),
       'name'               : fields.char    ('ID Number', size=32, required=True, translate=True),
       'active'             : fields.boolean ('Active'),
     }
     _defaults = {
       'active': lambda *a: True,
     }
     _order = "name"
res_partner_id_category()


class res_partner_id_number(osv.osv):
     _name = "res.partner.id_number"
     _columns = {
       'category_id'        : fields.many2one('res.partner.id_category','ID-Category', required=True),
       'name'               : fields.char    ('ID-Number',size=32,required=True),
       'partner_id'         : fields.many2one('res.partner','Partner', required=True),
       'partner_issued_id'  : fields.many2one('res.partner','Issued by', required=True),
       'date_issued'        : fields.date    ('Issued'),
       'valid_from'                : fields.date    ('Valid From'),
       'valid_until'            : fields.date    ('Valid Until'),
       'comment'            : fields.text    ('Notes'),
       'active'             : fields.boolean ('Active'),
       'state'              : fields.char    ('State', size=16),
     }
     _defaults = {
       'active': lambda *a: True,
     }
res_partner_id_number()

class res_partner(osv.osv):
      _inherit = "res.partner"
      _columns = {
          'id_numbers': fields.one2many('res.partner.id_number','partner_id','Identification Numbers'),
      }
res_partner()