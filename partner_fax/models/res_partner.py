# Copyright 2018 Apruzzese Francesco <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    fax = fields.Char()

    @api.onchange('fax', 'country_id', 'company_id')
    def _onchange_fax_validation(self):
        if self.fax:
            self.fax = self._phone_format(self.fax)
