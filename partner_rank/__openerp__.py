# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Savoir-faire Linux
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
    'name': 'Partner Rank',
    'version': '0.1',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'category': 'Customer Relationship Management',
    'summary': "Manage partner's priority",
    'description': """
Manage partner's priority
=========================

This module allow to setup a rank between partners, manually defined.
It adds :

1) a new field 'Rank' on the partner form
2) the ability to group the partners per rank
3) a new menu 'Sales -> Configuration -> Address Book -> Ranks'
    to define the available Ranks.

Each Rank is defined as :

* a priority (integer) : the lower the most important
* a name
* a description
* the name_get is defined as 'Priority - Name'

Contributors
------------
* El Hadji Dem (elhadji.dem@savoirfairelinux.com)
""",
    'depends': [
        'base',
    ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
        'res_partner_view.xml',
        'res_rank_view.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
