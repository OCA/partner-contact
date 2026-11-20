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

    @api.onchange("parent_id")
    def _onchange_owner_company_parent(self):
        if self.parent_id:
            self.owner_company_id = self.parent_id.owner_company_id

    @api.model_create_multi
    def create(self, vals_list):
        # Apply ownership inheritance to UI, import, and RPC creations alike.
        partners = super().create(vals_list)
        partners._sync_owner_company()
        return partners

    def write(self, vals):
        # A child cannot override the owner inherited from its parent.
        result = super().write(vals)
        if "parent_id" in vals or "owner_company_id" in vals:
            self._sync_owner_company()
        return result

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

    def _sync_owner_company(self):
        """Synchronize ownership from the root, one generation at a time."""
        roots = self
        if not self.env.context.get("_partner_owner_company_propagating"):
            roots = self.browse()
            # commercial_partner_id stops at child companies; ownership follows
            # the full parent hierarchy, including companies with a parent.
            for partner in self:
                root = partner
                while root.parent_id:
                    root = root.parent_id
                roots |= root
        for root in roots:
            children = self.with_context(active_test=False).search(
                [("parent_id", "=", root.id)]
            )
            if children:
                # Continue downward without restarting from the root on each write.
                children.with_context(_partner_owner_company_propagating=True).write(
                    {"owner_company_id": root.owner_company_id.id}
                )
