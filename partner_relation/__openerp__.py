# -*- encoding: utf-8 -*-
##############################################################################
#
#    Partner Relation module for Odoo
#    Copyright (C) 2014-2015 Artisanat Monastique de Provence (www.barroux.org)
#    Copyright (C) 2015 Akretion France (www.akretion.com)
#    @author: Alexis de Lattre <alexis.delattre@akretion.com>
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
    'name': 'Partner Relation',
    'version': '0.1',
    'category': 'Partner',
    'license': 'AGPL-3',
    'summary': 'Manage relations between partners',
    'author': 'Barroux Abbey, Akretion',
    'website': 'http://www.barroux.org',
    'depends': ['base'],
    'data': [
        'partner_relation_view.xml',
        'security/ir.model.access.csv',
        ],
    'demo': [
        'partner_relation_demo.xml',
        ],
    'test': ['test/relation.yml'],
    'installable': True,
}
