# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_use_partner_sector_for_person = fields.Boolean(
        'Use sector for individuals',
        help="Set if you want to be able to use sectors for "
             "individuals also.",
        implied_group='partner_sector.group_use_partner_sector_for_person')
