# -*- coding: utf-8 -*-
# Copyright 2016 Nicolas Bessi, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class BetterZip(models.Model):
    '''City/locations completion object'''

    _name = "res.better.zip"
    _description = __doc__
    _order = "name asc"
    _rec_name = "display_name"

    display_name = fields.Char('Name', compute='_get_display_name', store=True)
    name = fields.Char('ZIP')
    code = fields.Char('City Code', size=64,
                       help="The official code for the city")
    city = fields.Char('City', required=True)
    state_id = fields.Many2one('res.country.state', 'State')
    country_id = fields.Many2one('res.country', 'Country')
    latitude = fields.Float()
    longitude = fields.Float()

    @api.one
    @api.depends(
        'name',
        'city',
        'state_id',
        'country_id',
        )
    def _get_display_name(self):
        if self.name:
            name = [self.name, self.city]
        else:
            name = [self.city]
        if self.state_id:
            name.append(self.state_id.name)
        if self.country_id:
            name.append(self.country_id.name)
        self.display_name = ", ".join(name)

    @api.onchange('state_id')
    def onchange_state_id(self):
        if self.state_id:
            self.country_id = self.state_id.country_id
