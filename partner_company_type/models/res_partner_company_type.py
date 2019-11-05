# Copyright 2017-2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartnerCompanyType(models.Model):

    _name = "res.partner.company.type"
    _description = "Partner Company Type"

    name = fields.Char(string="Title", required=True, translate=True)
    shortcut = fields.Char(string="Abbreviation", translate=True)

    _sql_constraints = [
        ("name_uniq", "unique (name)", "Partner Company Type already exists!")
    ]
