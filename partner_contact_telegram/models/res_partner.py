import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    telegram_uid = fields.Char()
    telegram_alias = fields.Char()

    @api.model
    def create(self, vals):
        if vals.get("telegram_alias"):
            vals["telegram_alias"] = (
                vals["telegram_alias"].strip().replace(" ", "").lstrip("@")
            )

        return super().create(vals)

    def write(self, vals):
        if "telegram_alias" in vals and vals["telegram_alias"]:
            vals["telegram_alias"] = (
                vals["telegram_alias"].strip().replace(" ", "").lstrip("@")
            )

        return super().write(vals)

    @api.constrains("telegram_alias")
    def _check_telegram_alias(self):
        pattern = re.compile(r"^[a-zA-Z0-9_]{5,32}$")

        for partner in self:
            alias = (partner.telegram_alias or "").strip()

            if not alias:
                continue

            if not pattern.match(alias):
                raise ValidationError(
                    _(
                        "Telegram alias must be between 5 and 32 characters long,"
                        "and can only contain letters, numbers and underscores."
                    )
                )

            duplicate_alias = self.search(
                [
                    ("id", "!=", partner.id),
                    ("telegram_alias", "=ilike", alias),
                ],
                limit=1,
            )

            if duplicate_alias:
                raise ValidationError(
                    _("The alias is already in use by another partner.")
                )
