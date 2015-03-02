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

{
    "name": "Partner synchronization from OpenERP to ldap",
    "version": "1.2",
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "depends": ["base"],
    "category": "Generic Modules/Misc",
    "website": "http://www.camptocamp.com",
    "description": """

Live partner address synchronization through a LDAP module (inetOrgPerson).
OpenERP becomes the master of the LDAP. Each time an address is deleted,
created or updated the same is done in the ldap (a new record is pushed).
The LDAP configuration is done in the company view. There can be one different
LDAP per company. Do not forget to activate
the LDAP link in the configuration.
The used LDAP depends on the current user company.

This module does not allows bulk batching synchronisation into the LDAP and is
thus not suitable for an instant use with an existing LDAP.
In order to use it with an existing LDAP you have to alter the uid of contact
in your LDAP. The uid should be terp_ plus the OpenERP
contact id (for example terp_10).

N.B:
The module requires the python-ldap library
Unicode support --> As python ldap does not support unicode we try to decode
string if it fails we transliterate values.
Active Directory Support for Windows server 2003, try 2008 at your own risk
(AD support not tested for Version 6 of OpenERP looking for active dir test
infra)

""",
    "data": [
        "security/security.xml"
        'company_view.xml',
        'address_view.xml',
        "wizard.xml",
    ],
    "installable": False
}
