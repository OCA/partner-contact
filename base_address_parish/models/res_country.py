# Copyright 2022 Riverminds Cia Ltda - Mamfredy Mejia Matute
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Country(models.Model):
    _inherit = "res.country"

    enforce_parishes = fields.Boolean(
        help="Check this box to ensure every address created in that country has a "
        "Parish' chosen in the list of the city's parishes.",
    )
