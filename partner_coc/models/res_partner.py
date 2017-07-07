from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    coc_registration_number = fields.Char(
        string='CoC Registration Number',
        compute=lambda s: s._compute_identification(
            'coc_registration_number', 'coc',
        ),
        inverse=lambda s: s._inverse_identification(
            'coc_registration_number', 'coc',
        ),
        search=lambda s, *a: s._search_identification(
            'coc_registration_number', 'coc', *a
        ),
    )
