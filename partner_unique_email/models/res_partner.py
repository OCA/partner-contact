from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import config


class ResPartner(models.Model):
    _inherit = "res.partner"

    email = fields.Char(copy=False)

    @api.constrains("email")
    def check_unique_email(self):
        company_count = self.env["res.company"].sudo().search([])

        if config["test_enable"] and not self.env.context.get(
            "test_partner_email_unique"
        ):
            return

        for record in self:
            if len(company_count) == 1:
                res_partner_obj = (
                    self.env["res.partner"]
                    .sudo()
                    .search(
                        [
                            ("email", "=", record.email),
                            ("email", "!=", False),
                            ("id", "!=", self.id),
                            ("parent_id", "!=", self.id),
                        ]
                    )
                )
            else:
                res_partner_obj = (
                    self.env["res.partner"]
                    .sudo()
                    .search(
                        [
                            ("email", "=", record.email),
                            ("email", "!=", False),
                            ("id", "!=", self.id),
                            ("company_id", "=", self.env.company.id),
                            ("parent_id", "!=", self.id),
                        ]
                    )
                )

            if res_partner_obj:
                raise ValidationError(
                    _(
                        "Email %s already exist for %s."
                        % (str(record.email), str(res_partner_obj[0].name))
                    )
                )
