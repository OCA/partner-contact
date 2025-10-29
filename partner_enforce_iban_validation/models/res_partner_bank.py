# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, models
from odoo.exceptions import ValidationError
from odoo.tools import str2bool

from odoo.addons.base_iban.models.res_partner_bank import (
    _map_iban_template,
    validate_iban,
)

_logger = logging.getLogger(__name__)


class ResPartnerBank(models.Model):
    """
    Extend res.partner.bank to add configurable IBAN validation.

    Adds country-specific IBAN validation enforcement based on system parameters.
    Includes validation of IBAN country code matching bank/partner country.
    """

    _inherit = "res.partner.bank"

    def _get_validation_config(self):
        """
        Load validation configuration once to avoid repeated lookups.

        Returns:
            dict: Configuration dictionary with keys:
                - enforce (bool): Whether to enforce validation
                - bank_country_ids (list): List of bank country IDs to enforce
                - partner_country_ids (list): List of partner country IDs to enforce
        """
        ICP = self.env["ir.config_parameter"].sudo()
        Settings = self.env["res.config.settings"]

        return {
            "enforce": str2bool(
                ICP.get_param(
                    "partner_enforce_iban_validation.raise_exception", "false"
                )
            ),
            "bank_country_ids": Settings._load_iban_check_country_ids(
                self.env, "bank_country_ids"
            ),
            "partner_country_ids": Settings._load_iban_check_country_ids(
                self.env, "partner_country_ids"
            ),
        }

    def _validate_country_iban_match(self, country, iban_country_code, country_type):
        """
        Validate that IBAN country code matches the given country.

        This validation is only performed for countries that support IBAN format.
        If the country doesn't support IBAN, the validation is skipped.

        Args:
            country: Country record to validate against
            iban_country_code: Two-letter country code from IBAN
            country_type: 'bank' or 'partner' for error message

        Raises:
            ValidationError: country supports IBAN but doesn't match IBAN country code
        """
        if not country:
            return

        expected_country_code = country.code.lower()

        if expected_country_code not in _map_iban_template:
            # Country doesn't support IBAN - skip validation for this country
            return

        if iban_country_code != expected_country_code:
            raise ValidationError(
                _(
                    "IBAN country code %(iban_country)s does not match "
                    "%(country_type)s country %(expected_country)s.",
                    iban_country=iban_country_code.upper(),
                    country_type=country_type,
                    expected_country=expected_country_code.upper(),
                )
            )

    @api.constrains("acc_number", "partner_id", "bank_id")
    def _check_iban(self):
        """
        Validate IBAN with configurable enforcement.

        Applies IBAN validation based on system configuration:
        - Skips validation if skip_iban_validation context is set
        - If enforcement is disabled, uses standard Odoo validation (no exceptions)
        - If enforcement is enabled with country filters validates only matching records
        - If enforcement is enabled without filters, validates only records where the
          resolved country supports IBAN (same logic as base_iban)
        - Validates IBAN format before checking country code match
        - Raises ValidationError for enforced rec. with invalid IBAN or country mismatch
        """
        if self.env.context.get("skip_iban_validation"):
            return

        config = self._get_validation_config()

        # If enforcement is disabled, delegate all validation to parent
        if not config["enforce"]:
            return super()._check_iban()

        bank_country_ids = config["bank_country_ids"]
        partner_country_ids = config["partner_country_ids"]

        for record in self:
            iban = (record.acc_number or "").replace(" ", "")
            if not iban:
                continue

            # Step 1: Determine if this record should have enforced IBAN validation
            should_validate = False

            bank_country_match = (
                record.bank_id
                and record.bank_id.country
                and record.bank_id.country.id in bank_country_ids
            )

            partner_country_match = (
                record.partner_id
                and record.partner_id.country_id
                and record.partner_id.country_id.id in partner_country_ids
            )

            # IBAN prefix detection
            iban_country_code = iban[:2].lower() if len(iban) >= 2 else None
            iban_country_supported = (
                iban_country_code in _map_iban_template if iban_country_code else False
            )

            if not bank_country_ids and not partner_country_ids:
                # No country filters → validate based on bank country or IBAN prefix
                if record.bank_id and record.bank_id.country:
                    # Use bank country to decide validation
                    should_validate = (
                        record.bank_id.country.code.lower() in _map_iban_template
                    )
                else:
                    # No bank country → validate if IBAN prefix is supported
                    should_validate = iban_country_supported
            elif (
                bank_country_match or partner_country_match
            ) and iban_country_supported:
                # Filters set → enforce for matching records with supported IBAN prefix
                should_validate = True
            else:
                should_validate = False

            # Step 2: For enforced records, validate IBAN format and country match
            if should_validate:
                # Validate IBAN format first to ensure we have a valid country code
                try:
                    validate_iban(iban)
                except ValidationError as err:
                    raise ValidationError(
                        _(
                            "The IBAN %(iban)s is invalid. Please correct it "
                            "or disable validation in Settings.",
                            iban=iban,
                        )
                    ) from err

                # Only if IBAN format is valid, check country code match
                iban_country_code = iban[:2].lower()
                if record.bank_id and record.bank_id.country:
                    self._validate_country_iban_match(
                        record.bank_id.country, iban_country_code, "bank"
                    )
                if record.partner_id and record.partner_id.country_id:
                    self._validate_country_iban_match(
                        record.partner_id.country_id, iban_country_code, "partner"
                    )

        return
