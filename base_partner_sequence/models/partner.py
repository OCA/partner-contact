# -*- coding: utf-8 -*-
# © 2004-2009 Tiny SPRL (<http://tiny.be>).
# © 2013 initOS GmbH & Co. KG (<http://www.initos.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class ResPartner(models.Model):
    """Assigns 'ref' from a sequence on creation and copying"""

    _inherit = 'res.partner'

    @api.model
    def _needsRef(self, partner_id=None, vals=None):
        """
        Checks whether a sequence value should be assigned to a partner's 'ref'

        :param parnter_id: id of the partner object
        :param vals: known field values of the partner object
        :return: true iff a sequence value should be assigned to the\
                      partner's 'ref'
        """
        if not vals and not partner_id:
            raise Exception('Either field values or an id must be provided.')
        if vals is None:
            vals = {}
        values = vals.copy()
        # only assign a 'ref' to commercial partners
        if partner_id:
            partner = self.browse(partner_id)
            values.setdefault('is_company',  partner.is_company)
            values.setdefault('parent_id', partner.parent_id.id)
        return values.get('is_company') or not values.get('parent_id')

    @api.model
    def _commercial_fields(self):
        """
        Make the partner reference a field that is propagated
        to the partner's contacts
        """
        return super(ResPartner, self)._commercial_fields() + ['ref']

    @api.model
    def _get_next_ref(self, partner=None, vals=None):
        return self.env['ir.sequence'].get('res.partner')

    @api.model
    def create(self, vals):
        if not vals.get('ref') and self._needsRef(vals=vals):
            vals['ref'] = self._get_next_ref(vals=vals)
        return super(ResPartner, self).create(vals)

    @api.multi
    def write(self, vals):
        for partner in self:
            ref = vals.get('ref') if 'ref' in vals else partner.ref
            if not ref and self._needsRef(partner.id, vals):
                vals['ref'] = self._get_next_ref(partner, vals)
            super(ResPartner, partner).write(vals)
        return True

    @api.one
    def copy(self, default=None):
        default = default or {}
        if self._needsRef(self.id):
            default.update({
                'ref': self._get_next_ref(),
            })

        return super(ResPartner, self).copy(default)
