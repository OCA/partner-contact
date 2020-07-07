# Copyright 2017 Grant Thornton Spain - Ismael Calvo <ismael.calvo@es.gt.com>
# Copyright 2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import config


class ResPartner(models.Model):
    _inherit = 'res.partner'

    vat = fields.Char(copy=False)

    @api.constrains('vat', 'company_id')
    def _check_vat_unique(self):
        for record in self:
            if record.parent_id or not record.vat:
                continue
            test_condition = (config['test_enable'] and
                              not self.env.context.get('test_vat'))
            if test_condition:
                continue
            if self.env['res.partner'].sudo().with_context(
                active_test=False,
            ).search_count([
                ('parent_id', '=', False),
                ('vat', '=', record.vat),
                ('id', '!=', record.id),
                "|",
                ("company_id", "=", False),
                ("company_id", "=", record.company_id.id),
            ]):
                raise ValidationError((_(
                    "The VAT %s already exists in another "
                    "partner."
                ) + " " + _(
                    "NOTE: This partner may be archived."
                )) % record.vat)
