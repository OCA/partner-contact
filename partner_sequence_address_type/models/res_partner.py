from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _get_next_ref(self, vals=None):
        """
        Get the next reference according to the
        selected address type

        Still call super() to preserve the stack
        """
        super()._get_next_ref()

        partner_type = vals.get("type", self.type) if vals else self.type
        partner_sequence_id = self.env["res.partner.sequence.type"].search(
            [("code", "=", partner_type)]
        )
        return (
            partner_sequence_id.sequence_id.next_by_id()
            if partner_sequence_id.sequence_id
            else False
        )

    def _needs_ref(self, vals=None):
        """
        Return true even if it has a parent_id,
        or it's not a company

        Still call super() to preserve the stack
        """
        super()._needs_ref(vals)
        return True

    @api.model
    def _commercial_fields(self):
        """
        Don't make the partner reference a field that is propagated
        to the partner's contacts
        """
        return [i for i in super(ResPartner, self)._commercial_fields() if i != "ref"]
