# -*- coding: utf-8 -*-
# Copyright 2016 Nicolas Bessi, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResCompany(models.Model):

    _inherit = 'res.company'

    @api.onchange('better_zip_id')
    def on_change_city(self):
        if self.better_zip_id:
            self.zip = self.better_zip_id.name
            self.city = self.better_zip_id.city
            self.state_id = self.better_zip_id.state_id
            self.country_id = self.better_zip_id.country_id

    better_zip_id = fields.Many2one(
        'res.better.zip',
        string='Location',
        help='Use the city name or the zip code to search the location',
    )
