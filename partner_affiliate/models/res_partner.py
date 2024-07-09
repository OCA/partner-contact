# Copyright 2012 Camptocamp SA - Yannick Vaucher
# Copyright 2018 brain-tec AG - Raul Martin
# Copyright 2021 Therp BV - <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""Support affiliate relations beween partners."""

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


def check_if_parent_company(parent_type: str | None, vat: str | None):
    if parent_type== "parent_company" and not vat:
        raise ValidationError(_("Vat is mandatory to create a Parent Company"))

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
        compute="_compute_type",
        store=True
    )

    @api.depends("parent_id", "company_type", "name")
    def _compute_type(self):
        for partner in self:
            if partner.company_type == "person":
                partner.type = "contact"
                continue
            partner.type = "affiliate" if partner.parent_id else "parent_company"

    @api.onchange("city", "parent_id", "company_type")
    def _onchange_city(self):
        if self.type == "affiliate":
            self._get_affiliate_name()

    def _get_affiliate_name(self):
        self.ensure_one()
        parent_name = self.parent_id.name.upper() if self.parent_id else None
        city_name = self.city.upper() if self.city else None
        if parent_name and city_name:
            self.name = f"{parent_name} - {city_name}"
        else:
            self.name = parent_name or city_name
    
    def _fields_sync(self, values):
        """A company that will have a parent set, must be an affiliate,

        Setting a company to type affiliate, will automatically prevent
        overriding the address from the parent, because that is only done for
        contact partners.

        Clearing a parent_id from a company should reset its type to contact.

        You could argue that the same should be true for individuals.
        """
        if self.company_type == "person":
            desired_type = "contact"
        elif not self.parent_id and self.company_type == "company":
            desired_type = "parent_company"
        elif self.parent_id and self.company_type == "company":
            desired_type = "affiliate"
        else:
           desired_type = "contact"
        check_if_parent_company(desired_type, self.vat)
        if self.type != desired_type:
            super().write({"type": desired_type})
        return super()._fields_sync(values)

    @api.model
    def create(self, values):
        """ Il problema é che se é un'azienda fa un check e vuole la Pta Iva. Quindi si deve prima creare e poi sovrascrivere"""
        check_if_parent_company(values.get("type"), values.get("vat"))
        res =  super().create(values)
        if res.parent_id:
            res.vat = None
        return res


    @api.onchange("company_type")
    def onchange_get_partner_ids_domain(self):
        if self.company_type == 'person':
            domain = [('type','in', ['affiliate', 'parent_company'])]
        else:
            domain = [('type','=', 'parent_company')]
        return {'domain': {'parent_id': domain}}

    # @api.depends("company_type")
    # def get_partner_ids_domain(self):
    #     for partner in self:
    #         if partner.company_type == 'person':
    #             domain = [('type','in', ['affiliate', 'parent_company'])]
    #         else:
    #             domain = [('type','in', ['parent_company'])]
    #         partner.parent_id = str(domain)

