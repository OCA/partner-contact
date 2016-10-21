# -*- coding: utf-8 -*-
# © 2014-2016 Camptocamp SA
# @author: Nicolas Bessi
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResPartner(models.Model):
    """Add third field in address"""
    _inherit = "res.partner"

    street3 = fields.Char('Street 3')

    @api.model
    def _address_fields(self):
        fields = super(ResPartner, self)._address_fields()
        fields.append('street3')
        return fields


class ResCountry(models.Model):
    """Override default adresses formatting of countries"""
    _inherit = 'res.country'

    address_format = fields.Text(
        default=(
            "%(street)s\n%(street2)s\n%(street3)s\n"
            "%(city)s %(state_code)s %(zip)s\n"
            "%(country_name)s"
        )
    )
