# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    partner_email_check_syntax = fields.Boolean(
        string="Check syntax of email addresses",
        help="Don't allow email addresses with wrong syntax",
        default=True,
    )
    partner_email_check_filter_duplicates = fields.Boolean(
        string="Filter duplicate partner email addresses",
        help="Don't allow multiple partners to have the same email address.",
    )
    partner_email_check_duplicate_scope = fields.Selection(
        selection=[
            ("global", "Across all companies"),
            ("company", "Within the same company"),
        ],
        string="Duplicate email scope",
        default="global",
        required=True,
        help="Define which partners are compared when filtering duplicate email "
        "addresses:\n"
        "- Across all companies: an email address may only be used once in the "
        "whole database.\n"
        "- Within the same company: the same email address may be reused by a "
        "partner of another company, but must stay unique inside each company.",
    )
    partner_email_check_check_deliverability = fields.Boolean(
        string="Check deliverability of email addresses",
        help="Don't allow email addresses with providers that don't exist",
    )
