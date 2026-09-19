# Copyright 2025 Sylvain LE GAL (GRAP)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _
from odoo.exceptions import UserError
from odoo.http import request

from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.web.controllers import home

home.SIGN_UP_REQUEST_PARAMS |= {"firstname", "lastname"}


class PartnerFirstnameAuthSignupHome(AuthSignupHome):
    def _prepare_signup_values(self, qcontext):
        values = super()._prepare_signup_values(qcontext)
        if not values["is_company"]:
            values.update({key: qcontext.get(key) for key in ("firstname", "lastname")})
            values["name"] = request.env["res.users"]._get_computed_name(
                values.get("lastname"), values.get("firstname")
            )
            if not values["name"]:
                raise UserError(_("Please provide a firstname or a lastname."))
        return values

    def get_auth_signup_qcontext(self):
        qcontext = super().get_auth_signup_qcontext()
        ConfigSudo = request.env["ir.config_parameter"].sudo()
        config_required = ConfigSudo.get_param("partner_firstname.required_fields")
        config_first = ConfigSudo.get_param("partner_names_order")
        qcontext.update(
            {
                "firstname_required": config_required
                in ["firstname_lastname", "firstname"],
                "lastname_required": config_required
                in ["firstname_lastname", "lastname"],
                "lastname_first": config_first != "first_last",
            }
        )
        return qcontext
