# Copyright 2022 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from lxml import etree

from odoo import api, models

from odoo.addons.base.models.ir_ui_view import (
    transfer_modifiers_to_node,
    transfer_node_to_modifiers,
)


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        """We define the category_id field read-only if the user does not have
        permissions."""
        result = super().fields_view_get(view_id, view_type, toolbar, submenu)
        category_group = "partner_category_security.group_partner_category_user"
        if view_type == "form" and not self.env.user.has_group(category_group):
            doc = etree.XML(result["arch"])
            nodes = doc.xpath("//field[@name='category_id']")
            if nodes:
                nodes[0].set("readonly", "1")
                nodes[0].set("force_save", "1")
                modifiers = {}
                transfer_node_to_modifiers(nodes[0], modifiers)
                transfer_modifiers_to_node(modifiers, nodes[0])
            xarch, xfields = self.env["ir.ui.view"].postprocess_and_fields(
                doc, self._name
            )
            result["arch"] = xarch
            result["fields"] = xfields
        return result
