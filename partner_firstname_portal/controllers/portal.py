# Copyright 2025 Sylvain LE GAL (GRAP)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _
from odoo.http import request, route

from odoo.addons.portal.controllers.portal import CustomerPortal


def get_config_required():
    return (
        request.env["ir.config_parameter"]
        .sudo()
        .get_param("partner_firstname.required_fields")
    )


class PartnerFirstnameCustomerPortal(CustomerPortal):
    def _get_mandatory_fields(self):
        result = super()._get_mandatory_fields()
        if not request.env.user.partner_id.is_company:
            result.remove("name")
            config_required = get_config_required()
            if config_required in ("firstname", "lastname", "firstname_lastname"):
                result.extend(config_required.split("_"))
        return result

    def _get_optional_fields(self):
        result = super()._get_optional_fields()
        result += ["is_company", "name", "firstname", "lastname", "_pop_name_"]
        return result

    @route(["/my/account"], type="http", auth="user", website=True)
    def account(self, redirect=None, **post):
        if request.env.user.partner_id.is_company:
            post.pop("firstname", None)
            post.pop("lastname", None)
        else:
            # We use this trick to pop the name later,
            # in res.partner model, because core portal
            # module realize check on 'name' value
            request.update_context(name_field_pop_value=True)
        result = super().account(redirect=redirect, **post)
        return result

    def details_form_validate(self, data, partner_creation=False):
        error, error_message = super().details_form_validate(
            data, partner_creation=partner_creation
        )
        if (
            get_config_required() == "no"
            and not data.get("firstname")
            and not data.get("lastname")
            and not request.env.user.partner_id.is_company
        ):
            error["firstname"] = "error"
            error["lastname"] = "error"
            error_message.append(_("Please enter your firstname or your lastname."))
        return error, error_message
