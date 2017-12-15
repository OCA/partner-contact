# -*- coding: utf-8 -*-
# © 2014-2016 Camptocamp SA (Author: Romain Deheele)
# © 2017 senseFly, Amaris (Author: Quentin Theuret)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from odoo import fields


class Partner(models.Model):
    _inherit = 'res.partner'

    continent_id = fields.Many2one(
        'res.continent',
        related='country_id.continent_id',
        string='Continent',
        readonly=True,
        store=True,
    )
