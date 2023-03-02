# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class Contact(models.Model):
    _inherit = "res.partner"

    company_group_id = fields.Many2one(
        "res.partner", "Company group", domain=[("is_company", "=", True)]
    )
    company_group_member_ids = fields.One2many(
        comodel_name="res.partner",
        inverse_name="company_group_id",
        string="Company group members",
    )

    def _commercial_fields(self):
        return super()._commercial_fields() + ["company_group_id"]

    @api.onchange("company_group_id")
    def _onchange_company_group_id(self):
        res = {}
        if (
            self.company_group_id
            and self.company_group_id.property_product_pricelist
            != self.property_product_pricelist
        ):
            res["warning"] = {
                "title": _("Warning"),
                "message": _(
                    "The company group %s has the pricelist %s, that is different than"
                    " the pricelist set on this contact"
                )
                % (
                    self.company_group_id.display_name,
                    self.company_group_id.property_product_pricelist.display_name,
                ),
            }
        return res

    @api.onchange("property_product_pricelist")
    def _onchange_property_product_pricelist(self):
        res = self._onchange_company_group_id()
        if (
            not res
            and self.company_group_member_ids
            and self.company_group_member_ids.mapped("property_product_pricelist")
            - self.property_product_pricelist
        ):
            company_members = self.company_group_member_ids.filtered(
                lambda cm: cm.property_product_pricelist
                != self.property_product_pricelist
            )
            members_str = ""
            for member in company_members.sorted(key="display_name"):
                members_str += "\t- %s\n" % member.display_name
            res["warning"] = {
                "title": _("Warning"),
                "message": _(
                    "This contact has members of a company group with"
                    " different pricelists, the members are:\n%s"
                )
                % members_str,
            }
        return res
