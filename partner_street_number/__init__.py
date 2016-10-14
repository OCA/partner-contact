# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, an open source suite of business apps
#    This module copyright (C) 2013-2015 Therp BV (<http://therp.nl>).
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

from . import models
import logging
from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    """
    Post-install script. Because 'street' is now a stored function field, we
    should be able to retrieve its values from the cursor. We use those to
    fill the new name/number fields using the street field's inverse function,
    which does a basic street name/number split.
    """
    logging.getLogger('openerp.addons.partner_street_number').info(
        'Migrating existing street names')

    env = api.Environment(cr, SUPERUSER_ID, {})
    partners = env['res.partner'].search(
        [('street', '!=', False),
         ('street_name', '=', False)])

    for partner in partners:
        partner.sudo().write({'street': partner.street})
