# -*- encoding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
# Copyright (C) Odoo Colombia (Community).
# Authors       David Arnold (devCO)
#               Juan Pablo Aries (devCO)
#
# Co-Authors    Sandy Carter (Savaoirfairlinux)
#               El Hadji Dem (Savoirfairelinux)
#               Luis Miguel Varon
#               Hector Ivan Valencia (TIX)
#
# Collaborators Nhomar Hernandez (Vauxoo)
#               Humberto Ochoa (Vauxoo)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Partner Authentication with Fiscal Document',
    'description': """
* Keep track of due legal identification of partners with a \
corresponing document.
* Register additional document types within the GUI.
* Easy hook for custom copy and validation/formatting methods \
(res_partner_document.py)
""",
    'category': 'Localization',
    'license': 'AGPL-3',
    'author': 'Juan Pablo Arias (devCO), David Arnold BA HSG (devCO)',
    'website': '',
    'version': '0.3',
    'depends': [
        'base',
    ],
    'data': [
        'data/res.partner.idtype.csv',
        'res_partner_view.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}
