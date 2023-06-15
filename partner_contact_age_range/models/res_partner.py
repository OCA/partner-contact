# Copyright 2019-2020: Druidoo (<https://www.druidoo.io>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    age_range_id = fields.Many2one(
        "res.partner.age.range",
        "Age Range",
        compute="_compute_age_range_id",
        store=True,
    )

    @api.depends("age")
    def _compute_age_range_id(self):
        age_ranges = self.env["res.partner.age.range"].search([])
        for record in self:
            if record.age >= 0:
                age_range = age_ranges.filtered(
                    lambda age_range: age_range.age_from
                    <= record.age
                    <= age_range.age_to
                )
            else:
                age_range = self.env["res.partner.age.range"].browse()
            if record.age_range_id != age_range:
                record.age_range_id = age_range

    @api.model
    def _cron_update_age_range_id(self):
        """
        This method is called from a cron job.
        It is used to update age range on contact
        """
        partners = self.search([("birthdate_date", "!=", False)])
        partners._compute_age_range_id()
