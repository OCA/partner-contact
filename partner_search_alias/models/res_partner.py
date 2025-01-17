# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    search_alias = fields.Char(help="Enter the name that is also used for name search.")

    @property
    def _rec_names_search(self):
        return list(set(super()._rec_names_search + ["search_alias"]))

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        res = super().get_view(view_id, view_type, **options)
        if view_type == "search":
            xml = etree.XML(res["arch"])
            name_field = xml.xpath("//field[@name='name']")
            if name_field:
                name = name_field[0]
                filter_domain = name.get("filter_domain", "[]")
                filter_domain = filter_domain.replace(
                    "[", "['|', ('search_alias', 'ilike', self), "
                )
                name.set("filter_domain", filter_domain)
                res["arch"] = etree.tostring(xml)
        return res
