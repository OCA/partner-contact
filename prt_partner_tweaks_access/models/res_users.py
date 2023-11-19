# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    allowed_partner_category_ids = fields.Many2many(
        string="Allowed Partner Categories",
        comodel_name="res.partner.category",
        relation="prt_user_partner_category_rel",
        column1="user_id",
        column2="category_id",
    )

    allowed_country_ids = fields.Many2many(
        string="Allowed Countries",
        comodel_name="res.country",
        relation="prt_user_country_rel",
        column1="user_id",
        column2="country_id",
    )

    allowed_country_state_ids = fields.Many2many(
        string="Allowed States",
        comodel_name="res.country.state",
        relation="prt_user_country_state_rel",
        column1="user_id",
        column2="state_id",
    )

    @api.model
    def actived_predefined_rules_state(self):
        """Activate the predefined access rules"""
        self.env["ir.rule"].set_predefined_rules_state(False)

    # -- Write. Clear caches if related vals changed
    def write(self, vals):
        super(ResUsers, self).write(vals)
        if (
            "allowed_partner_category_ids" in vals
            or "allowed_country_ids" in vals
            or "allowed_country_state_ids" in vals
        ):
            self.clear_caches()
        return
