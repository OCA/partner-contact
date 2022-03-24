# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models


class Contact(models.Model):
    _inherit = "res.partner"

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
                    f"The company group {self.company_group_id.display_name} has the pricelist "
                    f"{self.company_group_id.property_product_pricelist.display_name}, "
                    "that is different than the pricelist set on this contact"
                ),
            }
        return res

    @api.onchange("property_product_pricelist")
    def _onchange_property_product_pricelist(self):
        res = self._onchange_company_group_id()
        if (
            not res
            and self.company_group_member_ids
            # Need to check _origin because the field company_group_ids is a recordset of
            # NewIds that have False values on the field property_product_pricelist.
            and self.company_group_member_ids._origin.mapped(
                "property_product_pricelist"
            )
            - self.property_product_pricelist
        ):
            company_members = self.company_group_member_ids.filtered(
                lambda cm: cm.property_product_pricelist
                != self.property_product_pricelist
            )
            members_str = ""
            for member in company_members:
                members_str += "\t- %s\n" % member.display_name
            res["warning"] = {
                "title": _("Warning"),
                "message": _(
                    "This contact has members of a company group with"
                    f" different pricelists, the members are:\n{members_str}"
                ),
            }
        return res
