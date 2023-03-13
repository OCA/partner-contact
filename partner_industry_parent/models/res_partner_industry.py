# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartnerIndustry(models.Model):
    _inherit = "res.partner.industry"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = "complete_name"
    _order = "complete_name"

    complete_name = fields.Char(
        compute="_compute_complete_name",
        store=True,
        recursive=True,
    )
    parent_path = fields.Char(index=True)
    parent_id = fields.Many2one(
        comodel_name="res.partner.industry", index=True, ondelete="cascade"
    )
    child_ids = fields.One2many(
        comodel_name="res.partner.industry",
        inverse_name="parent_id",
        string="Children Industry",
    )
    partner_count = fields.Integer(
        "# Partners",
        compute="_compute_partner_count",
        help="The number of partners under this industry "
        "(Does not consider the children categories)",
    )

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for industry in self:
            if industry.parent_id:
                industry.complete_name = "%s / %s" % (
                    industry.parent_id.complete_name,
                    industry.name,
                )
            else:
                industry.complete_name = industry.name

    def _compute_partner_count(self):
        read_group_res = self.env["res.partner"].read_group(
            [("industry_id", "child_of", self.ids)],
            ["industry_id"],
            ["industry_id"],
        )
        group_data = {
            data["industry_id"][0]: data["industry_id_count"] for data in read_group_res
        }
        for industry in self:
            partner_count = 0
            for sub_industry_id in industry.search(
                [("id", "child_of", industry.ids)]
            ).ids:
                partner_count += group_data.get(sub_industry_id, 0)
            industry.partner_count = partner_count

    @api.constrains("parent_id")
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_("You cannot create recursive categories."))

    @api.model
    def name_create(self, name):
        return self.create({"name": name}).name_get()[0]

    def name_get(self):
        if not self.env.context.get("hierarchical_naming", True):
            return [(record.id, record.name) for record in self]
        return super().name_get()
