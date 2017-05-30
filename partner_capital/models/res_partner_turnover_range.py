# -*- coding: utf-8 -*-
# Copyright 2015 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2015 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartnerTurnoverRange(models.Model):
    _name = 'res.partner.turnover_range'
    _description = "Turnover range"

    name = fields.Char(required=True, translate=True)
