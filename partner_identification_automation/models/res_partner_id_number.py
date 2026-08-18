from collections import defaultdict

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


def _get_new_date(base_date, number, unit):
    """Helper function to calculate new date based on number and unit."""
    if number is None or not unit:
        return base_date
    if unit == "days":
        return base_date + relativedelta(days=number)
    if unit == "weeks":
        return base_date + relativedelta(weeks=number)
    if unit == "months":
        return base_date + relativedelta(months=number)
    if unit == "years":
        return base_date + relativedelta(years=number)
    return base_date


class ResPartnerIdNumber(models.Model):
    _inherit = "res.partner.id_number"

    @api.model_create_multi
    def create(self, vals_list):
        """Extend create to calculate validity end date based on category defaults"""
        for vals in vals_list:
            # If valid_from is provided and no valid_until is specified,
            # calculate it from category defaults
            if (
                vals.get("valid_from")
                and not vals.get("valid_until")
                and vals.get("category_id")
            ):
                category = self.env["res.partner.id_category"].browse(
                    vals["category_id"]
                )
                if (
                    category.default_validity_number is not None
                    and category.default_validity_unit
                ):
                    start_date = fields.Date.from_string(vals["valid_from"])
                    end_date = _get_new_date(
                        start_date,
                        category.default_validity_number,
                        category.default_validity_unit,
                    )
                    vals["valid_until"] = end_date

        records = super().create(vals_list)
        return records

    @api.onchange("category_id", "valid_from")
    def _onchange_category_defaults(self):
        """Set default values based on category configuration"""
        if self.category_id:
            # Set default issuer if configured
            if self.category_id.default_issuer_id:
                self.partner_issued_id = self.category_id.default_issuer_id

            # Set default validity end date if valid_from is set
            if (
                self.valid_from
                and self.category_id.default_validity_number is not None
                and self.category_id.default_validity_unit
            ):
                start_date = self.valid_from
                end_date = _get_new_date(
                    start_date,
                    self.category_id.default_validity_number,
                    self.category_id.default_validity_unit,
                )
                self.valid_until = end_date  # Use valid_until instead of validity_end

    def _run_automatic_status_update(self):
        """Run automatic status updates for identification documents."""
        today = fields.Date.context_today(self)
        today_str = fields.Date.to_string(today)

        # Priority 1: Expired documents - documents with valid_until < today
        docs_to_expire = self.search(
            [["status", "!=", "close"], ["valid_until", "<", today_str]]
        )
        if docs_to_expire:
            docs_to_expire.write({"status": "close"})

        # Priority 2: To Renew documents - documents that are in the renewal window
        # Fetch only documents from categories with renewal settings
        docs_to_set_pending = self.env[self._name].browse()

        # Get categories that have renewal settings configured
        categories_with_renewal = self.env["res.partner.id_category"].search(
            [
                ("renewal_lead_number", ">", 0),
                ("renewal_lead_unit", "!=", False),
            ]
        )

        # Group categories by renewal settings to reduce number of search operations
        categories_by_renewal_key = defaultdict(
            lambda: self.env["res.partner.id_category"]
        )
        for category in categories_with_renewal:
            key = (category.renewal_lead_number, category.renewal_lead_unit)
            categories_by_renewal_key[key] |= category

        # Perform one search per group of categories with the same renewal settings
        for (number, unit), categories in categories_by_renewal_key.items():
            renewal_expiry_upper_bound = _get_new_date(today, number, unit)
            renewal_expiry_upper_bound_str = fields.Date.to_string(
                renewal_expiry_upper_bound
            )

            # Search for documents for all categories with the same renewal settings
            category_docs_to_renew = self.search(
                [
                    ["category_id", "in", categories.ids],
                    ["status", "in", ["draft", "open"]],
                    [
                        "valid_until",
                        ">",
                        today_str,
                    ],  # Not expired (today < valid_until)
                    [
                        "valid_until",
                        "<",
                        renewal_expiry_upper_bound_str,
                    ],  # valid_until < (today + renewal_period)
                    ["valid_from", "<=", today_str],  # Has started
                ]
            )

            docs_to_set_pending |= category_docs_to_renew

        if docs_to_set_pending:
            docs_to_set_pending.write({"status": "pending"})

        # Priority 3: Documents that should be opened (valid_from <= today <=
        # valid_until)
        docs_to_open = self.search(
            [
                ["status", "not in", ("open", "pending", "close")],
                ["valid_from", "<=", today_str],
                ["valid_until", ">=", today_str],
            ]
        )
        if docs_to_open:
            docs_to_open.write({"status": "open"})
