# -*- coding: utf-8 -*-
# Copyright 2013-2015 Therp BV (<http://therp.nl>)
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    """
    Post-install script. Because 'street' is now a stored function field, we
    should be able to retrieve its values from the cursor. We use those to
    fill the new name/number fields using the street field's inverse function,
    which does a basic street name/number split.
    """
    logging.getLogger('odoo.addons.partner_street_number').info(
        'Migrating existing street names')

    env = api.Environment(cr, SUPERUSER_ID, {})
    partners = env['res.partner'].with_context(active_test=False).search([
        ('street', '!=', False),
        ('street_name', '=', False)
    ])
    partners._write_street()
