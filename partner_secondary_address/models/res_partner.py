# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    has_secondary_address = fields.Boolean(
        string='Secondary Address',
        required=False)
    street_secondary = fields.Char()
    street2_secondary = fields.Char()
    zip_secondary = fields.Char(
        change_default=True)
    city_secondary = fields.Char()
    state_id_secondary = fields.Many2one(
        comodel_name='res.country.state',
        string='State (Secondary)',
        ondelete='restrict',
        domain="[('country_id', '=?', country_id)]")
    country_id_secondary = fields.Many2one(
        comodel_name='res.country',
        string='Country (Secondary)',
        ondelete='restrict')
