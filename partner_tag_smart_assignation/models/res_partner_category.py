# Copyright (C) 2019 Compassion CH (http://www.compassion.ch)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval


class ResPartnerCategory(models.Model):
    _inherit = "res.partner.category"

    tag_filter_condition_id = fields.Many2one(
        "ir.filters", "Domain filter", oldname="condition_id"
    )
    smart = fields.Boolean(
        help="Enable this to automatically assign the category on partners "
        "matching a given filter domain or SQL query."
    )
    tag_filter_partner_field = fields.Char(
        default="partner_id",
        oldname="partner_field",
        help="Relational field used on the filter object to find the partners.",
    )
    tag_filter_sql_query = fields.Text(
        "SQL query",
        help="Can be used instead of the filter for finding the relevant "
        "partners. The given SQL query should only return partner ids "
        "rows.",
    )
    tag_filter_join_operator = fields.Selection(
        [
            ("and", "AND (must satisfy both SQL and domain filter)"),
            ("or", "OR (can satisfy either SQL or domain filter)"),
        ],
        "JOIN operator",
        default="or",
        required=True,
    )
    partner_ids = fields.Many2many(
        "res.partner",
        "res_partner_res_partner_category_rel",
        "category_id",
        "partner_id",
    )

    tagged_partner_count = fields.Integer(
        compute="_compute_number_tags", stored=True, oldname="number_tags"
    )

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record.update_partner_tags()
        return record

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        if "tag_filter_condition_id" in vals or "model" in vals:
            self.update_partner_tags()
        return res

    @api.constrains(
        "tag_filter_condition_id",
        "tag_filter_condition_id.model_id",
        "tag_filter_condition_id.domain",
        "tag_filter_partner_field",
    )
    def check_condition(self):
        for me in self.filtered("tag_filter_condition_id"):
            if me.tag_filter_condition_id.model_id != "res.partner":
                model_link = self.env[me.tag_filter_condition_id.model_id]
                if me.tag_filter_partner_field not in model_link:
                    raise ValidationError(
                        "The chosen model has no field %s" % me.tag_filter_partner_field
                    )

    @api.constrains("tag_filter_sql_query")
    def check_sql_query(self):
        for me in self.filtered("tag_filter_sql_query"):
            self.env.cr.execute(me.tag_filter_sql_query)
            rows = self.env.cr.fetchall()
            for row in rows:
                if (
                    len(row) > 1
                    or not isinstance(row[0], int)
                    or not self.env["res.partner"].browse(row[0]).exists()
                ):
                    raise ValidationError(
                        "The SQL query should only return partner ids"
                    )

    @api.multi
    def update_partner_tags(self):
        for tagger in self.filtered("smart"):
            sql_partners = tagger.get_partners_from_sql()
            filter_partners = tagger.get_partners_from_ir_filter()
            if tagger.tag_filter_join_operator == "and":
                partners = sql_partners & filter_partners
            else:
                partners = sql_partners | filter_partners
            if partners:
                tagger.write({"partner_ids": [(6, 0, partners.ids)]})
            else:
                tagger.write({"partner_ids": [(5, 0, 0)]})
        return True

    def get_partners_from_ir_filter(self):
        self.ensure_one()
        if not self.tag_filter_condition_id.domain:
            return self.env["res.partner"]
        domain = safe_eval(
            self.tag_filter_condition_id.domain,
            locals_dict={"datetime": datetime},
            locals_builtins=True,
        )
        model = self.tag_filter_condition_id.model_id
        matching_records = self.env[model].search(domain)
        if matching_records:
            if model == "res.partner":
                partners = matching_records
            else:
                partners = matching_records.mapped(self.tag_filter_partner_field)
            return partners
        else:
            return self.env["res.partner"]

    def get_partners_from_sql(self):
        self.ensure_one()
        partner_obj = self.env["res.partner"]
        if not self.tag_filter_sql_query:
            return partner_obj
        self.env.cr.execute(self.tag_filter_sql_query)
        rows = self.env.cr.fetchall()
        if rows:
            return partner_obj.browse([r[0] for r in rows])
        else:
            return partner_obj

    @api.model
    def update_all_smart_tags(self):
        return self.search([("smart", "=", True)]).update_partner_tags()

    @api.depends("partner_ids")
    def _compute_number_tags(self):
        for category in self:
            category.tagged_partner_count = len(category.partner_ids)

    @api.multi
    def open_tags(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "res.partner",
            "view_type": "form",
            "view_mode": "list,form",
            "name": "Partners",
            "domain": [["id", "in", self.partner_ids.ids]],
        }
