# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.http import request, route

from odoo.addons.portal.controllers.portal import CustomerPortal


class PortalBlockEdit(CustomerPortal):
    def _prepare_portal_layout_values(self):
        """So we can change the edit link text in the view"""
        values = super()._prepare_portal_layout_values()
        values["block_portal_data_edit"] = request.env.user.block_portal_data_edit
        return values

    @route()
    def account(self, redirect=None, **post):
        """Inject a context that we later we catch in the template `render`"""
        if request.env.user.block_portal_data_edit:
            context = dict(request.env.context, block_portal_data_edit=True)
            request.env.context = context
        return super().account(redirect, **post)
