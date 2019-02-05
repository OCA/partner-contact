# Copyright 2017-2018 Onestein (<https://www.onestein.eu>)
# Copyright 2018 Therp BV (<https://www.therp.nl>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    coc_certificate_of_conduct = fields.Char(
        string='Certificate of Conduct',
        compute=lambda s: s._compute_identification(
            'coc_certificate_of_conduct', 'co_conduct',
        ),
        inverse=lambda s: s._inverse_identification(
            'coc_certificate_of_conduct', 'co_conduct',
        ),
        search=lambda s, *a: s._search_identification(
            'co_conduct', *a
        ),
    )
