# Copyright 2015 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCountry(models.Model):
    _inherit = "res.country"

    state_level = fields.Integer(help="Level for the state NUTS category.")
