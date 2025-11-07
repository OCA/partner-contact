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
        with_age = self.filtered(lambda x: x.age >= 0)
        ages = with_age.mapped("age")
        domain = (
            [
                ("age_from", "<=", max(ages)),
                ("age_to", ">=", min(ages)),
            ]
            if with_age
            else False
        )

        age_ranges = self.env["res.partner.age.range"].search(domain)

        for record in with_age:
            record.age_range_id = age_ranges.filtered(
                lambda age_range, record_data=record: age_range.age_from
                <= record_data.age
                <= age_range.age_to
            )

        (self - with_age).age_range_id = False

    @api.model
    def _cron_update_age_range_id(self):
        """
        This method is called from a cron job.
        It is used to update age range on contact
        """
        partners = self.search([("birthdate_date", "!=", False)])
        partners._compute_age_range_id()
