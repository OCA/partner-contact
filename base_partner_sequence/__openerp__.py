# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2013 initOS GmbH & Co. KG (<http://www.initos.com>).
#    Author Thomas Rehn <thomas.rehn at initos.com>
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
    "name": "Add a sequence on customers' code",
    "version": "1.1",
    "author": "initOS GmbH & Co. KG",
    "category": "Generic Modules/Base",
    "website": "http://www.initos.com",
    "depends": ["base"],
    "summary": "Sets customer's code from a sequence",
    "description": """
        This module adds the possibility to define a sequence for
        the partner code. This code is then set as default when you
        create a new customer or supplier, using the defined sequence.
        No codes are assigned for contacts such as shipping and
        invoice addresses.
        This module is a migration of the original base_partner_sequence
        addon to OpenERP version 7.0.
    """,
    "data": ['partner_sequence.xml'],
    "demo": [],
    "active": False,
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
