# Copyright 2017-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    coc_registration_number = fields.Char(
        string="CoC Registration Number",
        compute=lambda s: s._compute_identification("coc_registration_number", "coc"),
        inverse=lambda s: s._inverse_identification("coc_registration_number", "coc"),
        search=lambda s, *a: s._search_identification("coc", *a),
    )
