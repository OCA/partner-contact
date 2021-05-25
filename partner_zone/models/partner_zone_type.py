# Copyright 2021 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PartnerZoneType(models.Model):

    _name = 'partner.zone.type'
    _description = 'Partner Zone'

    name = fields.Char(
        string='Name',
        required=True,
    )

    zone_type = fields.Selection(
        selection=[]
    )
