# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    own_address = fields.Boolean(
        help="The contact keeps its own address: it is not copied from or to "
        "its parent company.",
    )

    def _has_own_address(self):
        self.ensure_one()
        return bool(self.own_address and self.parent_id and self.type == "contact")

    @api.depends("parent_id", "type", "own_address")
    def _compute_type_address_label(self):
        res = super()._compute_type_address_label()
        for partner in self.filtered(lambda p: p._has_own_address()):
            partner.type_address_label = self.env._("Address")
        return res

    @api.onchange("parent_id")
    def onchange_parent_id(self):
        result = super().onchange_parent_id()
        if self.own_address and result and "value" in result:
            address_fields = self._address_fields()
            result["value"] = {
                fname: value
                for fname, value in result["value"].items()
                if fname not in address_fields
            }
        return result

    def _get_address_values(self):
        # Empty while syncing a contact with its own address, so core does not
        # copy its address to the parent.
        if self and self.env.context.get("own_address_sync_id") in self.ids:
            return {}
        return super()._get_address_values()

    def _fields_sync(self, values):
        if self._has_own_address():
            self = self.with_context(own_address_sync_id=self.id)
        return super()._fields_sync(values)

    def _update_address(self, vals):
        own = self.filtered(lambda p: p._has_own_address())
        return super(ResPartner, self - own)._update_address(vals)

    def _handle_first_contact_creation(self):
        if self._has_own_address():
            return
        return super()._handle_first_contact_creation()

    def write(self, vals):
        if not vals and self.env.context.get("own_address_sync_id"):
            return True
        unflagged = self.browse()
        if "own_address" in vals and not vals["own_address"]:
            unflagged = self.filtered(lambda p: p._has_own_address())
        res = super().write(vals)
        for partner in unflagged.filtered(
            lambda p: p.parent_id and p.type == "contact"
        ):
            if address_values := partner.parent_id._get_address_values():
                partner.write(address_values)
        return res

    def _load_records_create(self, vals_list):
        # The batch import copies the parent address to every contact.
        partners = super()._load_records_create(vals_list)
        address_fields = self._address_fields()
        defaults = self.default_get(address_fields)
        for partner, vals in zip(partners, vals_list, strict=True):
            if partner._has_own_address():
                own_values = {
                    fname: vals.get(fname, defaults.get(fname, False))
                    for fname in address_fields
                }
                super(ResPartner, partner)._update_address(own_values)
        return partners
