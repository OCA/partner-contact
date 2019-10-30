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
    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda self: self.env['res.company']._company_default_get(
            'res.partner.company.type'
        ),
        ondelete='cascade',
    )

    _sql_constraints = [('name_uniq', 'unique (name)',
                         "Partner Company Type already exists!")]
