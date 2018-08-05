# -*- coding: utf-8 -*-
# Copyright 2018 Eficent Business and IT Consulting Services, S.L.

from openerp import fields, models


class SaleConfigSettings(models.TransientModel):
    _inherit = 'sale.config.settings'

    group_use_partner_sector_for_person = fields.Boolean(
        'Use sector for individuals',
        help="Set if you want to be able to use sectors for "
             "individuals also.",
        implied_group='partner_sector.group_use_partner_sector_for_person')
