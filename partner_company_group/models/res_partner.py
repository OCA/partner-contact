# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class Contact(models.Model):
    _inherit = 'res.partner'

    company_group_id = fields.Many2one(
        'res.partner',
        'Company group',
        domain=[('is_company', '=', True)]
    )

    @api.constrains('company_group_id')
    def _check_company_group_id(self):
        if not self._check_recursion('company_group_id'):
            raise ValidationError(
                _('Error! You cannot create recursive partner company group'))

    def _commercial_fields(self):
        return super()._commercial_fields() + ['company_group_id']
