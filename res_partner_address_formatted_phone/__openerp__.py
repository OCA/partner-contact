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

{
    "name" : "Format phone numbers of partner",
    "version" : "0.1",
    "author" : "Savoir-faire Linux",
    "website" : "http://www.savoirfairelinux.com",
    "license" : "AGPL-3",
    "category" : "Partner",
    "description" : """
This module formats the partner phone numbers based on the format of the 
phonenumbers library (http://pypi.python.org/pypi/phonenumbers).
    """,
    "images" : [],
    "depends" : ["base"],
    "demo" : [],
    "test" : [],
    "data" : [
        "res_partner_address_formatted_phone.xml",
        "res_country_phone_format_view.xml",
        "res_country_phone_format_data.xml",
    ],
    "installable": True,
    "complexity": "easy",
}
