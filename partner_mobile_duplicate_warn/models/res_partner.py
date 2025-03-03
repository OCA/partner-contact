# Copyright 2021-2022 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    same_mobile_partner_ids = fields.Many2many(
        "res.partner",
        compute="_compute_same_mobile_partner_ids",
        string="Partners with same mobile",
        compute_sudo=True,
    )

    @api.depends("mobile", "company_id")
    def _compute_same_mobile_partner_ids(self):
        # With phone_validation, the "mobile" field should be
        # clean in E.164 format, without any start/ending spaces
        # So we search on the 'mobile' field with '=' !
        for partner in self:
            same_mobile_partner_ids = False
            if partner.mobile:
                domain = [("mobile", "=", partner.mobile)]
                if partner.company_id:
                    domain += [
                        "|",
                        ("company_id", "=", False),
                        ("company_id", "=", partner.company_id.id),
                    ]
                partner_id = partner._origin.id
                if partner_id:
                    domain.append(("id", "!=", partner_id))
                same_mobile_partners = self.with_context(active_test=False).search(
                    domain
                )
                same_mobile_partner_ids = same_mobile_partners.ids or False
            partner.same_mobile_partner_ids = same_mobile_partner_ids

    def action_open_business_doc(self):
        """Method called when you click on the link in the duplicate warning banner"""
        # WARNING: the exact same method is provided by the modules
        # partner_email_duplicate_warn, l10n_fr_siret and certainly other modules
        # But, as these modules don't depend on each other, we need it here too.
        # Let's hope that in future versions of Odoo this method will be present
        # in the "base" module and we'll remove that code!
        self.ensure_one()
        action = {
            "name": _("Partners"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "views": [(False, "form")],
            "res_model": self._name,
            "res_id": self.id,
            "target": "current",
        }
        return action
