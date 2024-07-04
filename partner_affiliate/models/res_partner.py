# Copyright 2012 Camptocamp SA - Yannick Vaucher
# Copyright 2018 brain-tec AG - Raul Martin
# Copyright 2021 Therp BV - <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""Support affiliate relations beween partners."""

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    """Add relation affiliate_ids."""

    _name = "res.partner"
    _inherit = "res.partner"

    child_ids = fields.One2many(
        "res.partner",
        "parent_id",
        string="Contacts",
        domain=[
            ("active", "=", True),
            ("is_company", "=", False),
        ],
    )

    affiliate_ids = fields.One2many(
        "res.partner",
        "parent_id",
        string="Affiliates",
        domain=[
            ("active", "=", True),
            ("is_company", "=", True),
        ],
    )

    type = fields.Selection(
        selection_add=[
            ("affiliate", "Affiliate"),
            ("parent_company", "Parent Company"),
        ],
        required=True,
        default="contact",
        ondelete={
            "affiliate": "set default",
            "parent_company": "set default",
        },
    )

    parent_id_domain = fields.Many2many(
        comodel_name="res.partner",
        string="Parent Company Domain",
        compute="_compute_parent_id_domain",
        store=False,
    )

    @api.onchange("parent_id", "company_type")
    def _onchange_parent_id(self):
        for partner in self:
            if partner.company_type == "person":
                partner.type = "contact"
            if not partner.parent_id and partner.company_type == "company":
                partner.type = "parent_company"
            if partner.parent_id and partner.company_type == "company":
                partner.type = "affiliate"
                self.get_affiliate_name()

    @api.onchange("city")
    def _onchange_city(self):
        self.get_affiliate_name()

    def get_affiliate_name(self):
        parent_name = self.parent_id.name.upper() if self.parent_id.name else ""
        city_name = self.city.upper() if self.city else ""
        if parent_name and city_name:
            self.name = f"{parent_name} - {city_name}"
        else:
            self.name = parent_name or city_name

    @api.model
    def _fields_sync(self, values):
        """A company that will have a parent set, must be an affiliate,

        Setting a company to type affiliate, will automatically prevent
        overriding the address from the parent, because that is only done for
        contact partners.

        Clearing a parent_id from a company should reset its type to contact.

        You could argue that the same should be true for individuals.
        """
        # if self.is_company:
        #     desired_type = "affiliate" if self.parent_id else "contact"
        #     if self.type != desired_type:
        #         super().write({"type": desired_type})
        return super()._fields_sync(values)

    @api.model
    def create(self, values):
        res = super().create(values)
        self.check_if_parent_company(values)
        if res.parent_id:
            res.vat = None
            return res
        return res

    def check_if_parent_company(self, values):
        if values.get("type") == "parent_company":
            if not values.get("vat"):
                raise ValidationError(_("Vat is mandatory to create a Parent Company"))

    @api.depends("company_type")
    def _compute_parent_id_domain(self):
        for partner in self:
            if partner.company_type == "person":
                partner.parent_id_domain = [
                    ("type", "in", ["affiliate", "parent_company"])
                ]
            else:
                partner.parent_id_domain = [("type", "in", ["parent_company"])]
