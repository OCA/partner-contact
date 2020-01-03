# Copyright 2017-2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartnerCompanyType(models.Model):

    _name = 'res.partner.company.type'
    _description = 'Partner Company Type'

    name = fields.Char(
        string='Title',
        required=True,
        translate=True,
    )
    shortcut = fields.Char(
        string='Abbreviation',
        translate=True,
    )
    country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country",
        help="Allows this company type to be selected on partners from this "
        "country only. "
        "Leave it blank if you want it to appear on any partner.",
    )

    _sql_constraints = [('name_uniq', 'unique (name)',
                         "Partner Company Type already exists!")]
