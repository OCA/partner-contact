# Copyright 2019 Komit <https://komit-consulting.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from email_validator import EmailSyntaxError, EmailUndeliverableError, validate_email

from odoo import api, models
from odoo.exceptions import UserError, ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    def copy_data(self, default=None):
        res = super().copy_data(default=default)
        if self._should_filter_duplicates():
            for copy_vals in res:
                copy_vals.pop("email", None)
        return res

    @api.model
    def email_check(self, emails):
        return ",".join(
            self._normalize_email(email.strip())
            for email in emails.split(",")
            if email.strip()
        )

    @api.constrains("email")
    def _check_email_unique(self):
        if not self._should_filter_duplicates():
            return
        global_scope = self._should_filter_duplicates_globally()
        # Constraint methods run as superuser (see BaseModel._validate_fields),
        # so this search is authoritative across all records and companies,
        # regardless of the acting user's record rules. The acting user's own
        # access rights are only used to decide how much detail to disclose in
        # the error message.
        acting_user_model = self.sudo(False)
        for rec in self.filtered("email"):
            if "," in rec.email:
                raise UserError(
                    self.env._(
                        "Field contains multiple email addresses. This is "
                        "not supported when duplicate email addresses are "
                        "not allowed."
                    )
                )
            domain = [("email", "=", rec.email), ("id", "!=", rec.id)]
            if not global_scope:
                # Per-company scope: only records sharing the same company
                # (including company-agnostic records, company_id = False) are
                # considered duplicates.
                domain.append(("company_id", "=", rec.company_id.id))
            conflict = self.search(domain, limit=1)
            if not conflict:
                continue
            # Disclose the conflicting record only if the acting user is
            # actually allowed to see it; otherwise keep its identity private.
            if acting_user_model.search_count([("id", "=", conflict.id)], limit=1):
                raise UserError(
                    self.env._(
                        "Email address %(email)s is already in use by "
                        "%(partner)s (ID: %(partner_id)s). Please input "
                        "another email address or use the existing record.",
                        email=rec.email.strip(),
                        partner=conflict.display_name,
                        partner_id=conflict.id,
                    )
                )
            raise UserError(
                self.env._(
                    "Email address %(email)s is already in use by a record "
                    "you do not have access to. Please input a different "
                    "email address, or contact your system administrator to "
                    "request access.",
                    email=rec.email.strip(),
                )
            )

    def _normalize_email(self, email):
        if not self._should_check_syntax():
            return email
        try:
            result = validate_email(
                email,
                check_deliverability=self._should_check_deliverability(),
            )
        except EmailSyntaxError:
            raise ValidationError(
                self.env._("%s is an invalid email", email.strip())
            ) from EmailSyntaxError
        except EmailUndeliverableError:
            raise ValidationError(
                self.env._("Cannot deliver to email address %s", email.strip())
            ) from EmailUndeliverableError
        return result.normalized.lower()

    def _should_check_syntax(self):
        return self.env.company.partner_email_check_syntax

    def _should_filter_duplicates(self):
        return self.env.company.partner_email_check_filter_duplicates

    def _should_filter_duplicates_globally(self):
        return self.env.company.partner_email_check_duplicate_scope == "global"

    def _should_check_deliverability(self):
        return self.env.company.partner_email_check_check_deliverability

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("email"):
                vals["email"] = self.email_check(vals["email"])
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("email"):
            vals["email"] = self.email_check(vals["email"])
        return super().write(vals)
