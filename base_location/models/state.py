# Copyright 2016 Nicolas Bessi, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCountryState(models.Model):

    _inherit = 'res.country.state'

    better_zip_ids = fields.One2many('res.better.zip', 'state_id', 'Cities')
