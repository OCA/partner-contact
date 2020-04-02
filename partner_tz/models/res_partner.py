# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import fields, models


class ResPartner(models.Model):

    _inherit = 'res.partner'

    tz = fields.Selection(default=None)
