# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    This module copyright (C) 2015 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
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
    'name': 'Company Logo Secondary',
    'version': '1.0',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux, OCA',
    'category': 'Sales',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'description': """
Company Secondary Logo
======================

This module adds a a secondary logo to the company to be used by reports.
It requires the commit 491eb7ee35535666de6923ee63309c316b2b847d from the
https://github.com/savoirfairelinux/odoo/tree/7.0_res_company_secondary_logo
branch.

Contributors
------------
* Jordi Riera (jordi.riera@savoirfairelinux.com)
* Joao Alfredo Gama Batista (joao.gama@savoirfairelinux.com)
"""
    'depends': ['base'],
    'data': [
        'res_company_view.xml',
        'ir_actions_report_xml_view.xml'
    ],
    'installable': True,
}
