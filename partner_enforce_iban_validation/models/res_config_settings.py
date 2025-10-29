# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    """
    Extend system settings to configure IBAN validation behavior.

    Adds configuration options for country-specific IBAN validation enforcement.
    """

    _inherit = "res.config.settings"

    raise_exception_on_invalid_iban = fields.Boolean(
        string="Raise Exception on Incorrect IBAN",
        config_parameter="partner_enforce_iban_validation.raise_exception",
    )

    iban_bank_country_ids = fields.Many2many(
        "res.country",
        relation="iban_validation_bank_country_rel",
        column1="config_id",
        column2="country_id",
        string="Bank Countries",
    )

    iban_partner_country_ids = fields.Many2many(
        "res.country",
        relation="iban_validation_partner_country_rel",
        column1="config_id",
        column2="country_id",
        string="Partner Countries",
    )

    @staticmethod
    def _load_iban_check_country_ids(env, param_suffix):
        """
        Load country IDs from ir.config_parameter as list of integers.

        Args:
            env: Odoo environment
            param_suffix (str): Parameter suffix for the config parameter
                (e.g., 'bank_country_ids', 'partner_country_ids')

        Returns:
            list: List of country IDs as integers, empty list if no parameter set
        """
        param_value = (
            env["ir.config_parameter"]
            .sudo()
            .get_param(f"partner_enforce_iban_validation.{param_suffix}", "")
        )
        if not param_value:
            return []

        result = []
        for x in param_value.split(","):
            if not x.strip():
                continue
            try:
                result.append(int(x.strip()))
            except ValueError:
                _logger.warning(
                    "Invalid country ID '%s' found in parameter %s, skipping.",
                    x,
                    param_suffix,
                )
        return result

    @api.model
    def get_values(self):
        """
        Get configuration values including Many2many country fields.

        Returns:
            dict: Configuration values with country IDs loaded from parameters
        """
        res = super().get_values()
        res.update(
            {
                "iban_bank_country_ids": [
                    (
                        6,
                        0,
                        self._load_iban_check_country_ids(self.env, "bank_country_ids"),
                    )
                ],
                "iban_partner_country_ids": [
                    (
                        6,
                        0,
                        self._load_iban_check_country_ids(
                            self.env, "partner_country_ids"
                        ),
                    )
                ],
            }
        )
        return res

    def set_values(self):
        """
        Save configuration values including Many2many country fields.

        Returns:
            dict: Result of parent set_values method
        """
        res = super().set_values()
        icp = self.env["ir.config_parameter"].sudo()

        icp.set_param(
            "partner_enforce_iban_validation.bank_country_ids",
            ",".join(str(x) for x in self.iban_bank_country_ids.ids),
        )
        icp.set_param(
            "partner_enforce_iban_validation.partner_country_ids",
            ",".join(str(x) for x in self.iban_partner_country_ids.ids),
        )
        return res
