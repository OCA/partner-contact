# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


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
            price_list = self.company_group_id.property_product_pricelist
            res["warning"] = {
                "title": self.env._("Warning"),
                "message": self.env._(
                    "The company group %(company_group)s has"
                    " the pricelist %(pricelist)s, that is different"
                    " than the pricelist set on this contact"
                )
                % {
                    "company_group": self.company_group_id.display_name,
                    "pricelist": price_list.display_name,
                },
            }
        return res

    @api.onchange("property_product_pricelist")
    def _onchange_property_product_pricelist(self):
        res = self._onchange_company_group_id()
        if (
            not res
            and self.company_group_member_ids
            # Need to check _origin because the field company_group_ids is a recordset
            # of NewIds that have False values on the field property_product_pricelist.
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
            for member in company_members.sorted(key="display_name"):
                members_str += f"\t- {member.display_name}\n"
            res["warning"] = {
                "title": self.env._("Warning"),
                "message": self.env._(
                    "This contact has members of a company group with"
                    f" different pricelists, the members are:\n{members_str}"
                ),
            }
        return res
