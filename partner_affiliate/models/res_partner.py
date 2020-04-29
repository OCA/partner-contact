# Copyright 2012 Camptocamp SA - Yannick Vaucher
# Copyright 2018 brain-tec AG - Raul Martin
# Copyright 2020 Therp BV - <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ResPartner(models.Model):
    """Add relation affiliate_ids."""
    _inherit = "res.partner"

    type = fields.Selection(selection_add=[('affiliate', 'Affiliate')])

    # force "active_test" domain to bypass _search() override
    child_ids = fields.One2many(
        'res.partner', 'parent_id',
        string='Contacts',
        domain=[('active', '=', True), ('is_company', '=', False)],
    )
    # force "active_test" domain to bypass _search() override
    affiliate_ids = fields.One2many(
        'res.partner', 'parent_id',
        string='Affiliates',
        domain=[('active', '=', True), ('is_company', '=', True)],
    )

    def get_original_address(self):
        def convert(value):
            return value.id if isinstance(value, models.BaseModel) else value

        result = {
            'value': {key: convert(self[key]) for key in self._address_fields()}
        }
        return result

    @api.onchange('parent_id')
    def onchange_parent_id(self):
        """Keep the original address info to set it back if its a company."""
        original_address = self.get_original_address()
        new_partner = super(ResPartner, self).onchange_parent_id()
        # When the affiliate is a company, we must set back its address
        # because the super call changes its address by the new parent address.
        # In addition, the type must be set to affiliate instead of contact.
        if new_partner and self.is_company:
            new_partner.update(original_address)
            new_partner['value'].update({'type': 'affiliate'})
        return new_partner
