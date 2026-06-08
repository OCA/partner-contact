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
    same_email_inaccessible_count = fields.Integer(
        compute="_compute_same_email_partner_ids",
        string="Partners with same e-mail you cannot access",
        compute_sudo=True,
    )

    @api.depends("email", "company_id")
    def _compute_same_email_partner_ids(self):
        for partner in self:
            same_email_partner_ids = []
            inaccessible_count = 0
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
                matches = search_partners.filtered(
                    lambda p, email=partner_email: p.email
                    and p.email.strip().lower() == email
                )
                # This field is computed as superuser (compute_sudo), so the
                # match set may include partners the acting user cannot read.
                # Only expose the readable ones as links; rendering the others
                # would raise an AccessError when the web client fetches their
                # display_name. The rest are merely counted so the banner can
                # warn about them without disclosing their identity.
                readable = matches.with_env(self.env(su=False))._filtered_access("read")
                same_email_partner_ids = readable.ids
                inaccessible_count = len(matches) - len(readable)
            partner.same_email_partner_ids = same_email_partner_ids or False
            partner.same_email_inaccessible_count = inaccessible_count

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
