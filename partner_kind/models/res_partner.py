# Copyright 2023 Akretion (https://www.akretion.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):

    _inherit = ["res.partner"]

    kind = fields.Selection(
        selection="_get_partner_kind",
        string="Type",
        help="Type of partner",
        readonly=False,
        compute="_compute_kind",
        default="company",
        compute_sudo=True,
        required=True,
        store=True,
    )

    def _get_partner_kind(self):
        return [
            ("user", _("User")),
            ("address", _("Address")),
            ("person", _("Individual")),
            ("company", _("Company")),
        ]

    @api.depends("user_ids", "user_ids.active", "parent_id", "is_company")
    def _compute_kind(self):
        self._get_default_kind()

    def _get_default_kind(self):
        for rec in self:
            if any(rec.user_ids.mapped("active")):
                rec.kind = "user"
            elif rec.parent_id:
                rec.kind = "address"
            elif rec.is_company:
                rec.kind = "company"
            elif not rec.is_company:
                rec.kind = "person"

    @api.constrains("kind")
    def _check_valid_kind(self):
        if self._context.get("skip_kind_check"):
            return
        for rec in self:
            if rec.kind == "user" and not any(rec.user_ids.mapped("active")):
                raise ValidationError(_("User type is only for users"))
            elif rec.kind == "address" and not rec.parent_id:
                raise ValidationError(_("Company field is mandatory for address type"))
