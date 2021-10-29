# Copyright 2012 Camptocamp SA - Yannick Vaucher
# Copyright 2018 brain-tec AG - Raul Martin
# Copyright 2021 Therp BV - <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""Support affiliate relations beween partners."""

from odoo import fields, models, api


class ResPartner(models.Model):
    """Add relation affiliate_ids."""
    _inherit = "res.partner"

    type = fields.Selection(selection_add=[("affiliate", "Affiliate")])

    # force "active_test" domain to bypass _search() override
    child_ids = fields.One2many(
        "res.partner",
        "parent_id",
        string="Contacts",
        domain=[("active", "=", True), ("is_company", "=", False)],
    )
    # force "active_test" domain to bypass _search() override
    affiliate_ids = fields.One2many(
        "res.partner",
        "parent_id",
        string="Affiliates",
        domain=[("active", "=", True), ("is_company", "=", True)],
    )

    @api.multi
    def _fields_sync(self, values):
        """A company that will have a parent set, must be an affiliate,

        Setting a company to type affiliate, will automatically prevent
        overriding the address from the parent, because that is only done for
        contact partners.

        Clearing a parent_id from a company should reset its type to contact.

        You could argue that the same should be true for individuals.
        """
        if self.is_company:
            desired_type = "affiliate" if self.parent_id else "contact"
            if self.type != desired_type:
                super().write({"type": desired_type})
        return super()._fields_sync(values)
