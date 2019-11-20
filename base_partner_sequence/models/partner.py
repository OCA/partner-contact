# Copyright 2004-2009 Tiny SPRL (<https://tiny.be>).
# Copyright 2013 initOS GmbH & Co. KG (<https://www.initos.com>).
# Copyright 2016 Tecnativa - Vicent Cubells
# Copyright 2016 Camptocamp - Akim Juillerat (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, models


class ResPartner(models.Model):
    """Assigns 'ref' from a sequence on creation and copying"""

    _inherit = "res.partner"

    def _get_next_ref(self, vals=None):
        return self.env["ir.sequence"].next_by_code("res.partner")

    @api.model
    def create(self, vals):
        if not vals.get("ref") and self._needs_ref(vals=vals):
            vals["ref"] = self._get_next_ref(vals=vals)
        return super(ResPartner, self).create(vals)

    def copy(self, default=None):
        default = default or {}
        if self._needs_ref():
            default["ref"] = self._get_next_ref()
        return super(ResPartner, self).copy(default=default)

    def write(self, vals):
        for partner in self:
            partner_vals = vals.copy()
            if (
                not partner_vals.get("ref")
                and partner._needs_ref(vals=partner_vals)
                and not partner.ref
            ):
                partner_vals["ref"] = partner._get_next_ref(vals=partner_vals)
            super(ResPartner, partner).write(partner_vals)
        return True

    def _needs_ref(self, vals=None):
        """
        Checks whether a sequence value should be assigned to a partner's 'ref'

        :param vals: known field values of the partner object
        :return: true iff a sequence value should be assigned to the\
                      partner's 'ref'
        """
        if not vals and not self:  # pragma: no cover
            raise exceptions.UserError(
                _("Either field values or an id must be provided.")
            )
        # only assign a 'ref' to commercial partners
        if self:
            vals = {}
            vals["is_company"] = self.is_company
            vals["parent_id"] = self.parent_id
        return vals.get("is_company") or not vals.get("parent_id")

    @api.model
    def _commercial_fields(self):
        """
        Make the partner reference a field that is propagated
        to the partner's contacts
        """
        return super(ResPartner, self)._commercial_fields() + ["ref"]
