# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010 Camptocamp SA (http://www.camptocamp.com) 
# All Right Reserved
#
# Author : Nicolas Bessi (Camptocamp), Joel Grand-Guillaume
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
    "name" : "Partner Adress Category",
    "description" : """Add categories on Address like there is on Partner. This is interesting for managing mailling list based on address
    for example.
 """,
    "version" : "1.2",
    "author" : "Camptocamp",
    "category" : "Generic Modules/Base",
    "website": "http://www.camptocamp.com",
    "depends" : [
                    "base",
                ],
    "init_xml" : [
                    "security/security.xml"
                 ],
    "update_xml" : [
                    "base_address_view.xml",
                    'security/ir.model.access.csv',
                   ],
    "active": False,
    "installable": True
}
