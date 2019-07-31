# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    type = fields.Selection(selection_add=[('brand', 'Brand')])
