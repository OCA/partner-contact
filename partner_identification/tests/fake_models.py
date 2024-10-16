# Copyright 2017 LasLabs Inc.
# Copyright 2018 ACSONE
# Copyright 2018 Camptocamp
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    _description = "Fake Model"

    social_security = fields.Char(
        compute=lambda s: s._compute_identification("social_security", "SSN"),
        inverse=lambda s: s._inverse_identification("social_security", "SSN"),
        search=lambda s, *a: s._search_identification("SSN", *a),
    )
