# Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    duns = fields.Char(
        string="DUNS",
        help="Data Universal Numbering System",
        copy=False,
    )
    same_duns_partner_id = fields.Many2one(
        comodel_name="res.partner",
        compute="_compute_same_duns_partner_id",
        string="Partner with same DUNS",
    )

    @api.depends("duns", "company_id")
    def _compute_same_duns_partner_id(self):
        for partner in self:
            if not partner.duns or partner.parent_id:
                partner.same_duns_partner_id = False
                continue
            # NOTE: use _origin to deal with onchange()
            partner_id = partner._origin.id
            domain = [
                ("duns", "=", partner.duns),
                ("company_id", "in", [False, partner.company_id.id]),
            ]
            if partner_id:
                domain += [
                    ("id", "!=", partner_id),
                    "!",
                    ("id", "child_of", partner_id),
                ]
            # NOTE: active_test=False because if a partner has been deactivated you
            # still want to show the warning, so that you can reactivate it instead
            # of creating a new one, which would loose its history.
            Partner = self.with_context(active_test=False).sudo()
            partner.same_duns_partner_id = Partner.search(domain, limit=1)

    @api.model
    def _sanitize_duns(self, duns):
        return duns and "".join(filter(str.isdigit, duns))

    @api.onchange("duns")
    def _onchange_duns(self):
        for rec in self:
            sanitized = rec._sanitize_duns(rec.duns)
            if rec.duns != sanitized:
                rec.duns = sanitized

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "duns" in vals:
                vals["duns"] = self._sanitize_duns(vals["duns"])
        return super().create(vals_list)

    def write(self, vals):
        if "duns" in vals:
            vals["duns"] = self._sanitize_duns(vals["duns"])
        return super().write(vals)
