# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):

    _inherit = 'res.partner'

    alias_ids = fields.One2many(
        string='Aliases',
        comodel_name='res.partner.alias',
        inverse_name='partner_id',
    )
