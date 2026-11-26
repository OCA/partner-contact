# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    phone2 = fields.Char(
        "Phone (Secondary)",
        compute="_compute_phone2",
        inverse="_inverse_phone2",
        readonly=False,
        store=True,
    )

    def _get_partner_phone2_update(self, force_void=True):
        self.ensure_one()
        if (
            self.partner_id
            and (force_void or self.phone2)
            and self.phone2 != self.partner_id.phone2
        ):
            lead_phone2_formatted = (
                self._phone_format(fname="phone2") or self.phone2 or False
            )
            partner_phone2_formatted = (
                self.partner_id._phone_format(fname="phone2")
                or self.partner_id.phone2
                or False
            )
            return lead_phone2_formatted != partner_phone2_formatted
        return False

    def _inverse_phone2(self):
        for lead in self:
            if lead._get_partner_phone2_update(force_void=False):
                lead.partner_id.phone2 = lead.phone2

    @api.depends("partner_id.phone2")
    def _compute_phone2(self):
        for lead in self:
            if lead.partner_id.phone2 and lead._get_partner_phone2_update():
                lead.phone2 = lead.partner_id.phone2

    def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
        res = super()._prepare_customer_values(
            partner_name, is_company=is_company, parent_id=parent_id
        )
        res["phone2"] = self.phone2
        return res
