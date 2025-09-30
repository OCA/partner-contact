# Copyright 2017-2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartnerCompanyType(models.Model):

    _name = "res.partner.company.type"
    _description = "Partner Company Type"
    _rec_name = "display_name"
    _rec_names_search = ["name", "shortcut"]

    name = fields.Char(string="Title", required=True, translate=True)
    shortcut = fields.Char(string="Abbreviation", translate=True)
    display_name = fields.Char(string="Display name", compute="_compute_display_name")

    _sql_constraints = [
        ("name_uniq", "unique (name)", "Partner Company Type already exists!")
    ]

    @api.depends("name", "shortcut")
    def _compute_display_name(self):
        for partner_company_type in self:
            partner_company_type.display_name = (
                partner_company_type.shortcut + " - " + partner_company_type.name
            )
