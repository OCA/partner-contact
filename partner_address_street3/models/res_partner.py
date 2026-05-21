# Copyright 2014-2020 Camptocamp SA
# @author: Nicolas Bessi
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo import api, fields, models


class ResPartner(models.Model):
    """Add third field in address"""

    _inherit = "res.partner"

    street3 = fields.Char("Street 3")

    @api.model
    def _address_fields(self):
        res = super()._address_fields()
        res.append("street3")
        return res

    @api.model
    def default_get(self, default_fields):
        values = super().default_get(default_fields)
        parent_id = self.env.context.get("default_parent_id") or values.get("parent_id")
        if parent_id:
            parent = self.browse(parent_id)
            for field in self._address_fields():
                if field in default_fields and not values.get(field):
                    val = parent[field]
                    values[field] = val.id if isinstance(val, models.BaseModel) else val
        return values

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        res = super().get_view(view_id=view_id, view_type=view_type, **options)
        if view_type == "form":
            doc = etree.XML(res["arch"])
            for node in doc.xpath("//field[@name='child_ids']"):
                context = node.get("context")
                if not context:
                    node.set("context", "{'default_street3': street3}")
                elif "default_street3" not in context:
                    context_str = context.strip()
                    if context_str.endswith("}"):
                        new_context = context_str[:-1] + ", 'default_street3': street3}"
                        node.set("context", new_context)
            res["arch"] = etree.tostring(doc, encoding="unicode")
        return res

    def _display_address(self, without_company=False):
        """Remove empty lines which can happen when street3 field is empty."""
        res = super()._display_address(without_company=without_company)
        while "\n\n" in res:
            res = res.replace("\n\n", "\n")
        return res
