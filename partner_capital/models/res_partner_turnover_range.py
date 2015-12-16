# -*- coding: utf-8 -*-
#    Copyright (c) 2015 Antiun Ingeniería S.L. (http://www.antiun.com)
#                       Antonio Espinosa <antonioea@antiun.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResPartnerTurnoverRange(models.Model):
    _name = 'res.partner.turnover_range'
    _description = "Turnover range"

    name = fields.Char(required=True, translate=True)
