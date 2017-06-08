# -*- encoding: utf-8 -*-
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


{
	'name': 'blacklist partner',
	'version': '1.0',
	'category': 'Generic Modules/Others',
	'description': """
	This module allows you to add a category 'blacklist' in the form of your customers.
	If a customer is in this category it will appear in red in OpenERP.
	""",
	'author': 'BHC',
	'website': 'www.bhc.com/',
	'depends': ['base','sale','warning'], 
	'images': ['images/customer.png','images/customer_tree.png','images/sale_order.png'],
	'init_xml': [],
	'update_xml': ['partner_listing.xml'],
	'demo_xml': [],
	'installable': True,
	'active': False,
}

