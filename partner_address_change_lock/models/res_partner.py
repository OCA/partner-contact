# Copyright 2026 Akretion (https://www.akretion.com).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from markupsafe import Markup, escape

from odoo import _, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import format_datetime


class ResPartner(models.Model):
    _inherit = "res.partner"

    address_history_html = fields.Html(
        string="Address History",
        readonly=True,
        sanitize=False,
    )

    def _get_all_address_fields(self):
        return ["street", "street2", "zip", "city", "state_id", "country_id"]

    def _get_locked_address_fields(self):
        if self.env.company.partner_address_lock_mode == "country":
            return ["country_id"]
        elif self.env.company.partner_address_lock_mode == "any_address_field":
            return self._get_all_address_fields()
        return []

    def _has_blocking_condition(self):
        self.ensure_one()
        unpaid = self.env["account.move"].search_count(
            [
                ("partner_id", "=", self.id),
                (
                    "move_type",
                    "in",
                    ["out_invoice", "out_refund", "in_invoice", "in_refund"],
                ),
                ("payment_state", "not in", ["paid", "reversed"]),
                ("state", "=", "posted"),
            ]
        )
        return bool(unpaid)

    def _build_address_html_block(self):
        self.ensure_one()

        parts = [
            self.street,
            self.street2,
            " ".join(filter(None, [self.zip, self.city])),
            self.state_id.name if self.state_id else "",
            self.country_id.name if self.country_id else "",
        ]

        address_lines = "<br/>".join(
            escape(p.strip()) for p in parts if p and p.strip()
        )

        date_str = format_datetime(self.env, fields.Datetime.now())

        html = """
        <div style="
            margin-bottom: 10px;
            padding: 10px;
            border-left: 4px solid #875a7b;
            background: #f8f9fa;
            border-radius: 4px;
        ">
            <div style="font-size: 12px; color: #666; margin-bottom: 6px;">
                🕒 {date_str}
            </div>
            <div style="font-size: 14px; line-height: 1.4;">
                {address_lines}
            </div>
        </div>
        """

        return Markup(
            html.format(
                date_str=date_str,
                address_lines=address_lines,
            )
        )

    def _effective_change(self, vals, fields):
        for field in fields:
            if self._fields[field].type == "many2one":
                current_id = self[field].id if self[field] else None
                new_id = vals[field] if vals[field] else None
                if field in vals and new_id != current_id:
                    return True
            else:
                return True
        return False

    def _append_address_history(self):
        for rec in self:
            block = rec._build_address_html_block()
            existing = rec.address_history_html or ""
            rec.with_context(skip_address_history=True).write(
                {"address_history_html": Markup(block) + Markup(existing)}
            )

    def write(self, vals):
        res = super().write(vals)
        if self.env.context.get("skip_address_history"):
            return res
        locked_fields = self._get_all_address_fields()
        changed = [f for f in locked_fields if f in vals]
        changed_locked = any(f in self._get_locked_address_fields() for f in changed)

        if changed_locked:
            for rec in self:
                if rec._has_blocking_condition() and rec._effective_change(
                    vals, changed
                ):
                    raise ValidationError(
                        _(
                            "You cannot modify the address of partner "
                            '"%s" because they have unpaid invoices'
                        )
                        % (rec.name)
                    )
            self._append_address_history()
        return res
