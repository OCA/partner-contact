# -*- coding: utf-8 -*-
# Copyright 2017 Franco Tampieri, Freelancer http://franco.tampieri.info
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCountryState(models.Model):

    _inherit = 'res.country'

    geonames_state_name = fields.Integer(
        u'Geoname State Name Column',
        default=3,
    )
    geonames_state_code = fields.Integer(
        u'Geoname State Code Column',
        default=4,
    )
