# Copyright 2025 Sylvain LE GAL (GRAP)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.web.controllers import home

home.SIGN_UP_REQUEST_PARAMS |= {"company_type"}


class PartnerIsCompanyAuthSignupHome(AuthSignupHome):
    def _prepare_signup_values(self, qcontext):
        values = super()._prepare_signup_values(qcontext)
        values.update({"is_company": qcontext.get("company_type") == "company"})
        return values
