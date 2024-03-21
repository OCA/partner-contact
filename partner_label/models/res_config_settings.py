# Copyright 2017-2019 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    partner_labels_width = fields.Float(
        related="company_id.partner_labels_width",
        required=True,
        readonly=False,
    )
    partner_labels_height = fields.Float(
        related="company_id.partner_labels_height",
        required=True,
        readonly=False,
    )
    partner_labels_padding = fields.Float(
        related="company_id.partner_labels_padding",
        required=True,
        readonly=False,
    )
    partner_labels_margin_top = fields.Float(
        related="company_id.partner_labels_margin_top",
        required=True,
        readonly=False,
    )
    partner_labels_margin_bottom = fields.Float(
        related="company_id.partner_labels_margin_bottom",
        required=True,
        readonly=False,
    )
    partner_labels_margin_left = fields.Float(
        related="company_id.partner_labels_margin_left",
        required=True,
        readonly=False,
    )
    partner_labels_margin_right = fields.Float(
        related="company_id.partner_labels_margin_right",
        required=True,
        readonly=False,
    )
    partner_labels_paperformat_id = fields.Many2one(
        "report.paperformat",
        string="Paperformat",
        required=True,
        default=lambda self: self.env.ref(
            "partner_label.report_res_partner_label"
        ).paperformat_id,
        compute="_compute_partner_labels_paperformat_id",
        inverse="_inverse_partner_labels_paperformat_id",
    )

    def _compute_partner_labels_paperformat_id(self):
        for this in self:
            this.partner_labels_paperformat_id = self.env.ref(
                "partner_label.report_res_partner_label"
            ).paperformat_id

    def _inverse_partner_labels_paperformat_id(self):
        for this in self:
            self.env.ref(
                "partner_label.report_res_partner_label"
            ).paperformat_id = this.partner_labels_paperformat_id

    def action_partner_labels_preview(self):
        return self.env.ref("partner_label.report_res_partner_label").report_action(
            self.env["res.partner"].search([], limit=100),
        )
