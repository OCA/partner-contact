# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons.base.models.res_partner import _lang_get


class ResCountry(models.Model):
    _inherit = "res.country"

    lang = fields.Selection(
        _lang_get,
        string="Enforce language",
        help="This country partners' language will be set to this value by default",
    )
