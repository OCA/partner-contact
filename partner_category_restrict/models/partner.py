# Copyright 2023 Akretion (https://www.akretion.com).
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.constrains("category_id")
    def _check_category_restrict_filter(self):
        for record in self:
            for categ in record.category_id.filtered("restrict_filter_id"):
                restrict_domain = categ.restrict_filter_id.sudo()._get_eval_domain()
                if not self.env["res.partner"].search_count(
                    [("id", "=", record.id)] + restrict_domain
                ):
                    raise UserError(
                        _(
                            'The tag "{}" cannot be applied to the partner "{}".\n'
                            '\nCause: it does not respect the "{}" filter.\n'
                            "\nDetail: {}"
                        ).format(
                            categ.name,
                            record.name,
                            categ.restrict_filter_id.name,
                            restrict_domain,
                        )
                    )
