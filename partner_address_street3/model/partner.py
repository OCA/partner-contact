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
