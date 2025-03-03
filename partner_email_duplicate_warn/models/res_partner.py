# Copyright 2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    same_email_partner_ids = fields.Many2many(
        "res.partner",
        compute="_compute_same_email_partner_ids",
        string="Partner with same e-mail",
        compute_sudo=True,
    )

    @api.depends("email", "company_id")
    def _compute_same_email_partner_ids(self):
        for partner in self:
            same_email_partner_ids = []
            if partner.email and partner.email.strip():
                partner_email = partner.email.strip().lower()
                domain = [("email", "=ilike", "%" + partner_email + "%")]
                if partner.company_id:
                    domain += [
                        "|",
                        ("company_id", "=", False),
                        ("company_id", "=", partner.company_id.id),
                    ]
                partner_id = partner._origin.id
                if partner_id:
                    domain += [
                        ("id", "!=", partner_id),
                        "!",
                        ("id", "child_of", partner_id),
                        "!",
                        ("id", "parent_of", partner_id),
                    ]
                search_partners = self.with_context(active_test=False).search(domain)
                for search_partner in search_partners:
                    if (
                        search_partner.email
                        and search_partner.email.strip().lower() == partner_email
                    ):
                        same_email_partner_ids.append(search_partner.id)
            partner.same_email_partner_ids = same_email_partner_ids or False

    def action_open_business_doc(self):
        """Method called when you click on the link in the duplicate warning banner"""
        # WARNING: the exact same method is provided by the modules
        # partner_mobile_duplicate_warn, l10n_fr_siret and certainly other modules
        # But, as these modules don't depend on each other, we need it here too.
        # Let's hope that in future versions of Odoo this method will be present
        # in the "base" module and we'll remove that code!
        self.ensure_one()
        action = {
            "name": self.env._("Partners"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "views": [(False, "form")],
            "res_model": self._name,
            "res_id": self.id,
            "target": "current",
        }
        return action
