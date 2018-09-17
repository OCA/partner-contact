# Copyright 2016 Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    partner_ref_unique = fields.Selection(
        selection=[
            ('none', 'None'),
            ('companies', 'Only companies'),
            ('all', 'All partners'),
        ], string="Unique partner reference for", default="none")
