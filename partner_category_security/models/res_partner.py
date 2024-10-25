# Copyright 2022 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from lxml import etree

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        """We define the category_id field read-only if the user does not have
        permissions."""
        result = super().get_view(view_id, view_type, **options)
        category_group = "partner_category_security.group_partner_category_user"
        if view_type == "form" and not self.env.user.has_group(category_group):
            doc = etree.XML(result["arch"])
            nodes = doc.xpath("//field[@name='category_id']")
            if nodes:
                nodes[0].set("readonly", "1")
                nodes[0].set("force_save", "1")
            result["arch"] = etree.tostring(doc, encoding="unicode")
        return result
