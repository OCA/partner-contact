# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info("Move brands to res.brand model")
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        brands = env['res.partner'].search([('type', '=', 'brand')])
        for brand in brands:
            env['res.brand'].create({'partner_id': brand.id})
            brand.type = 'contact'
