# Copyright 2022 Riverminds Cia Ltda - Mamfredy Mejia Matute
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from lxml import etree

from odoo import api, models, fields
from odoo.tools.translate import _


class Partner(models.Model):
    _inherit = 'res.partner'

    country_enforce_parishes = fields.Boolean(related='country_id.enforce_parishes', readonly=True)
    parish_id = fields.Many2one('res.parish', string='Parish')

    @api.onchange('parish_id')
    def _onchange_parish_id(self):
        if self.parish_id:
            self.zip = self.parish_id.code
            self.city_id = self.parish_id.city_id
            self.state_id = self.parish_id.state_id
        elif self._origin:
            self.city_id = False
            self.zip = False
            self.state_id = False