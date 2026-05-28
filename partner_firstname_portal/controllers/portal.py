# Copyright 2025 Sylvain LE GAL (GRAP)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


def get_config_required():
    return (
        request.env["ir.config_parameter"]
        .sudo()
        .get_param("partner_firstname.required_fields")
    )


class PartnerFirstnameCustomerPortal(CustomerPortal):
    def _create_or_update_address(
        self,
        partner_sudo,
        address_type="billing",
        use_delivery_as_billing=False,
        callback="/my/addresses",
        required_fields=False,
        verify_address_values=True,
        **form_data,
    ):
        if partner_sudo.is_company:
            form_data.pop("firstname", None)
            form_data.pop("lastname", None)
        else:
            partner_sudo = partner_sudo.with_context(name_field_pop_value=True)
        return super()._create_or_update_address(
            partner_sudo,
            address_type,
            use_delivery_as_billing,
            callback,
            required_fields,
            verify_address_values,
            **form_data,
        )

    def _validate_address_values(
        self, address_values, partner_sudo, address_type, *args, **kwargs
    ):
        invalid_fields, missing_fields, error_messages = (
            super()._validate_address_values(
                address_values, partner_sudo, address_type, *args, **kwargs
            )
        )
        required_fields = get_config_required()
        if "firstname" in required_fields and not kwargs.get("firstname"):
            missing_fields.add("firstname")
            error_messages.append(self.env._("Firstname is missing."))
        if "lastname" in required_fields and not kwargs.get("lastname"):
            missing_fields.add("lastname")
            error_messages.append(self.env._("Lastname is missing."))
        if (
            "no" == required_fields
            and not kwargs.get("firstname")
            and not kwargs.get("lastname")
            and not partner_sudo.is_company
        ):
            error_messages.append(
                self.env._("Please enter your firstname or your lastname.")
            )
            missing_fields.add("firstname")
            missing_fields.add("lastname")
        return invalid_fields, missing_fields, error_messages

    def _handle_extra_form_data(self, extra_form_data, address_values):
        res = super()._handle_extra_form_data(extra_form_data, address_values)
        data = {}
        if extra_form_data.get("firstname"):
            data["firstname"] = extra_form_data["firstname"]
        if extra_form_data.get("lastname"):
            data["lastname"] = extra_form_data["lastname"]
        if data:
            partner = self.env.user.partner_id
            partner.write(data)
        return res
