# Copyright 2024 Akretion France (www.akretion.com)
# @author: Syera BONNEAUX <syera.bonneaux@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models, fields, api


class PartnerTitle(models.Model):
    _inherit = 'res.partner.title'

    active = fields.Boolean(string='Active', default=True)