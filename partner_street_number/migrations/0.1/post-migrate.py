# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013-2014 Therp BV (<http://therp.nl>).
#
#    @autors: Stefan Rijnhart, Ronald Portier
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
import logging
from openerp import pooler, SUPERUSER_ID


def migrate(cr, version):
    """
    Post-install script. If version is not set, we are called at installation
    time. Because 'street' is now a stored function field, we should be able
    to retrieve its values from the cursor. We use those to fill the new
    name/number fields using the street field's inverse function, which does
    a basic street name/number split.
    """
    if version:
        return
    logging.getLogger('openerp.addons.partner_street_number').info(
        'Migrating existing street names')
    cr.execute(
        'SELECT id, street FROM res_partner '
        'WHERE street IS NOT NULL and street_name IS NULL'
        )
    partner_obj = pooler.get_pool(cr.dbname)['res.partner']
    for partner in cr.fetchall():
        partner_obj.write(
            cr, SUPERUSER_ID, partner[0], {'street': partner[1]})
