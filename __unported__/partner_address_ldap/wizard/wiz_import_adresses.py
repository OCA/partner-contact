# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010 Camptocamp SA (http://www.camptocamp.com)
# All Right Reserved
#
# Author : Vincent Renaville
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

#  init_import.py
#
#  Created by Nicolas Bessi on 28.04.09.
#  Copyright (c) 2009 CamptoCamp. All rights reserved.
#

import base64
import unicodedata
import re
import wizard
from openerp import pooler
from openerp import netsvc
from openerp.tools.translate import _
from openerp.tools import ustr

_FORM = '''<?xml version="1.0"?>
<form string="Export addresses to ldap">
</form>'''


_FORM1 = """<?xml version="1.0"?>
<form string="Export log">
<separator colspan="4" string="Clic on 'Save as' to save the log file :" />
    <field name="errors"/>
</form>
"""

_FIELDS = {
    'errors': {
        'string': 'Error report',
        'type': 'binary',
        'readonly': True,
    },
}


# As this is a bulk batch wizard the performance process was not really
# taken in account ###
# The ideal way of doing would be to modify the  connexion settings in
# order to have a connexion singleton in the file partner.py it will
# avoid connexion renegotiation for each partner.
def _action_import_addresses(self, cr, uid, data, context):
    """ This function create or update each addresses present in the database.
    It will also generate an error report"""
    logger = netsvc.Logger()
    error_report = [u'Error report']
    add_obj = pooler.get_pool(cr.dbname).get('res.partner.address')
    add_ids = add_obj.search(cr, uid, [])
    addresses = add_obj.browse(cr, uid, add_ids)
    phone_fields = ['phone', 'fax', 'mobile', 'private_phone']
    for add in addresses:
        vals = {
            'partner_id': add.partner_id.id,
            'email': add.email,
            'phone': add.phone,
            'fax': add.fax,
            'mobile': add.mobile,
            'firstname': add.firstname,
            'lastname': add.lastname,
            'private_phone': add.private_phone,
            'street': add.street,
            'street2': add.street2,
            'city': add.city,
        }
        # Validating the mail
        if add.email:
            if re.match(
                    "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\."
                    "([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", add.email) is None or\
               re.search(u"[éèàêöüäï&]", add.email) is not None:
                msg = _(
                    'Address %s for partner  %s has email that is invalid %s'
                ) % (
                    ustr(vals['firstname']) + ' ' + ustr(vals['lastname']),
                    add.partner_id.name,
                    ustr(add.email)
                )
                logger.notifyChannel('ldap export', netsvc.LOG_INFO, msg)
                error_report.append(msg)
                vals['email'] = False
        # Validating the Phone
        for key in phone_fields:
            if (not ustr(vals[key]).startswith('+')
                    or ustr(vals[key]).find("\n") != -1
                    or re.search(u"[éèàêöüä#&]", ustr(vals[key])) is not None):
                vals[key] = False
                msg = _(
                    'Address %s for partner  %s has %s that is invalid '
                ) % (
                    ustr(vals['firstname']) + ' ' + ustr(vals['lastname']),
                    add.partner_id.name,
                    key
                )
                logger.notifyChannel('ldap export', netsvc.LOG_INFO, msg)
                error_report.append(msg)
        # Validating the CN
        if not add.lastname and add.firstname:
            msg = (_('!!! Address %s for partner %s has no last name and '
                     'first name that is valid partner name was used')
                   % (ustr(add.id), add.partner_id.name))
            logger.notifyChannel('ldap export', netsvc.LOG_INFO, msg)
            error_report.append(msg)
        # We save to LDAP
        add.write(vals, {'init_mode': True})
    # we by pass the encoding errors
    map(lambda x: unicodedata.normalize("NFKD", x).encode('ascii', 'ignore'),
        error_report)
    error_report = "\n".join(error_report)
    logger.notifyChannel("MY TOPIC", netsvc.LOG_ERROR, error_report)
    try:
        data = base64.encodestring(error_report.encode())
    except:
        data = base64.encodestring("Could not generate report file. "
                                   "Please look in the log for details")

    return {'errors': data}


class Wiz_import_addresses(wizard.interface):
    states = {
        'init': {
            'actions': [],
            'result': {
                'type': 'form',
                'arch': _FORM,
                'fields': {},
                'state': [
                    ('end', 'Cancel'),
                    ('importadd', 'Export adresses into company LDAP')
                ]
            }
        },
        'importadd': {
            'actions': [_action_import_addresses],
            'result': {
                'state': [('end', 'OK', 'gtk-ok', True)],
                'arch': _FORM1,
                'fields': _FIELDS,
                'type': 'form'
            }
        }
    }
Wiz_import_addresses('ldap.import_adresses')
