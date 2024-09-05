# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    search_alias = fields.Char(help="Enter the name that is also used for name search.")

    @property
    def _rec_names_search(self):
        return list(set(super()._rec_names_search + ["search_alias"]))
