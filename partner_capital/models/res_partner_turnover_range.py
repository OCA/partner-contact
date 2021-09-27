# Copyright 2015 Tecnativa - Antonio Espinosa
# Copyright 2015 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartnerTurnoverRange(models.Model):
    _name = "res.partner.turnover_range"
    _description = "Turnover range"

    name = fields.Char(required=True, translate=True)
