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

from openerp.osv import orm, fields


class Res_company(orm.Model):
    """Define ldap connexion parameters"""

    _inherit = 'res.company'
    _columns = {
        'base_dn': fields.char(
            'User dn',
            size=128,
            help="Example: cn=contacts_admin,dc=ldap,dc=dcc2c"
        ),
        'contact_dn': fields.char(
            'Bind dn',
            size=128,
            help="Example: dc=ldap,dc=dcc2c -- watch out "
                 "the OU will be automatically included inside"
        ),
        'ounit': fields.char(
            'Contact Organizational unit of the contacts',
            size=128,
            help="Example: Contacts"
        ),
        'ldap_server': fields.char(
            'Server address',
            size=128,
            help="Example: ldap.camptocamp.com"
        ),
        'passwd': fields.char(
            'ldap password',
            size=128,
            help="Example: Mypassword1234"
        ),
        'ldap_active': fields.boolean(
            'Activate ldap link for this company',
            help='If not check nothing will be reported into the ldap'
        ),
        'is_activedir': fields.boolean(
            'Active Directory ?',
            help='The ldap is part of an Active Directory'
        ),
        'ldap_port': fields.integer(
            'LDAP Port',
            help="If not specified, the default port(389), will be used"
        ),
    }
