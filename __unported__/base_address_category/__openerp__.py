# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010-2013 Camptocamp SA (http://www.camptocamp.com)
# All Right Reserved
#
# Author : Nicolas Bessi (Camptocamp), Joel Grand-Guillaume
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

{
    "name": "Partner Address Category",
    "description": """\
 res.partner.address.category
 ----------------------------

 This module is deprecated as of OpenERP 7.0, because that version
 deprecated res.partner.address, and res.partner already has multi
 category support (visible as Tags in the user interface).

 The port of this module to OpenERP 7 keeps the model definitions, but
 removes the views (for which the base views are no longer
 available). The migration process should ensure that the
 res.partner.address.category records are migrated to
 res.partner.category records.
 """,
    "version": "1.2",
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "category": "Generic Modules/Base",
    "website": "http://www.camptocamp.com",
    "depends": [
        "base",
    ],
    "data": [
        "security/security.xml"
        'security/ir.model.access.csv',
    ],
    "installable": False,
}
