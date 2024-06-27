# Copyright 2012 Camptocamp SA - Yannick Vaucher
# Copyright 2018 brain-tec AG - Raul Martin
# Copyright 2021 Therp BV - <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""Support affiliate relations beween partners."""

from odoo import api, fields, models


class ResPartner(models.Model):
    """Add relation affiliate_ids."""

    _name = "res.partner"
    _inherit = "res.partner"

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

    is_registered_office = fields.Boolean(
        compute="_compute_is_registered_office", stored=True
    )

    type = fields.Selection(selection_add=[("affiliate", "Affiliate")])

    # force "active_test" domain to bypass _search() override

    @api.depends("vat")
    def _compute_is_registered_office(self):
        for record in self:
            if not record.vat:
                record.is_registered_office = False
            else:
                record.is_registered_office = True

    @api.model
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

    @api.onchange("parent_id")
    def _onchange_parent_id(self):
        for rec in self:
            if rec.parent_id:
                rec.type = "affiliate"
            else:
                rec.type = "contact"
