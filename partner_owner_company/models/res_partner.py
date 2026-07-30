# Copyright 2026 Open Source Integrators
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.osv import expression


class ResPartner(models.Model):
    _inherit = "res.partner"

    owner_company_id = fields.Many2one(
        "res.company",
        string="Owner Company",
        help="Company that owns this contact. This is a soft alternative to company_id "
        "that doesn't enforce access security but allows tracking company belonging.",
        index=True,
    )

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        """
        Override name_search to prioritize current company contacts unless:
        - Full name match
        - Exact code/ref match
        - Exact email match
        """
        args = args or []
        # For partial matches, prioritize current company contacts
        # Logic: Show contacts where:
        #   1. Contact belongs to current company, OR
        #   2. Contact's parent belongs to current company, OR
        #   3. Contact has no owner company AND
        #      (no parent OR parent has no owner company)
        current_company = self.env.company.id
        belongs_to_company = expression.OR(
            [
                [("owner_company_id", "parent_of", [current_company])],
                [("parent_id.owner_company_id", "parent_of", [current_company])],
            ]
        )
        no_company_owner = expression.AND(
            [
                [("owner_company_id", "=", False)],
                expression.OR(
                    [
                        [("parent_id", "=", False)],  # Top-level contact
                        [
                            ("parent_id.owner_company_id", "=", False)
                        ],  # Parent has no owner
                    ]
                ),
            ]
        )
        owner_args = expression.OR([belongs_to_company, no_company_owner])
        res = super().name_search(
            name, expression.AND([owner_args, args]), operator, limit
        )

        # If not result, try exact matches (bypasses company filtering)
        # Check if search term matches full name, exact code, or exact email
        if name and not res:
            exact_match_domain = [
                "|",
                ("name", "=ilike", name),
                "|",
                ("ref", "=ilike", name),
                "|",
                ("email", "=ilike", name),
                ("vat", "=ilike", name),
            ]
            res = super().name_search(name, exact_match_domain + args, operator, limit)

        return res
