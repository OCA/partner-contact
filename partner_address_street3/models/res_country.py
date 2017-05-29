# -*- coding: utf-8 -*-
# Copyright 2014 Nicolas Bessi, Alexandre Fayolle, Camptocamp SA
# Copyright 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


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
