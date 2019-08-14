# Copyright (C) 2019 Le Filament
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    type = fields.Selection(selection_add=[('postal', 'Postal address')])
