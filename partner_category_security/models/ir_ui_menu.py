# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models, tools


class IrUiMenu(models.Model):
    _inherit = "ir.ui.menu"

    @api.model
    @tools.ormcache("frozenset(self.env.user.groups_id.ids)", "debug")
    def _visible_menu_ids(self, debug=False):
        """It is not possible to set !groups in menu items, we do not return the record
        if the user has base.group_system (to avoid the 'duplicate' menu)."""
        visible = super()._visible_menu_ids(debug=debug)
        user = self.env.user
        if (
            self.env.su
            or user.has_group("base.group_system")
            or user.has_group("sales_team.group_sale_manager")
        ):
            menu_partner_category_custom = self.env.ref(
                "partner_category_security.menu_partner_category_custom"
            )
            if menu_partner_category_custom.id in visible:
                visible.remove(menu_partner_category_custom.id)
        return visible
