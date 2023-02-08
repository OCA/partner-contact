from odoo import api, fields, models


class MergePartnerLine(models.TransientModel):
    _inherit = "base.partner.merge.line"
    _order = "aggr_ids_count asc, min_id asc"

    aggr_ids_count = fields.Integer(
        "Total Aggr IDs", compute="_compute_aggr_ids_count", store=True
    )

    @api.depends("aggr_ids")
    def _compute_aggr_ids_count(self):
        for record in self:
            record.aggr_ids_count = len(record.aggr_ids)
