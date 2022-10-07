# Copyright 2022 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import requests
import xmltodict

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class USPSAddressPartner(models.Model):
    _inherit = "res.partner"

    usps_date_validation = fields.Date(
        "Last Validation Date",
        readonly=True,
        copy=False,
        help="The date the address was last validated by USPS and accepted",
    )

    def button_usps_address_validation(self):
        view_ref = self.env.ref(
            "partner_usps_address_validation.usps_address_validation_view_form"
        )
        ctx = self.env.context.copy()
        ctx.update({"active_ids": self.ids, "active_id": self.id})
        return {
            "type": "ir.actions.act_window",
            "name": "USPS Address Validation",
            "binding_view_types": "form",
            "view_mode": "form",
            "view_id": view_ref.id,
            "res_model": "usps.address.validation",
            "nodestroy": True,
            "res_id": False,
            "target": "new",
            "context": ctx,
        }

    def cleanse_address(self, response_data):
        response_data = response_data.get("AddressValidateResponse").get("Address")
        if response_data.get("Address1") != "FALSE":
            a1 = response_data.get("Address1")
        else:
            a1 = " "
        if response_data.get("Address2") != "FALSE":
            a2 = response_data.get("Address2")
        else:
            a2 = " "
        if response_data.get("City") != "FALSE":
            city = response_data.get("City")
        else:
            city = " "
        if response_data.get("State") != "FALSE":
            state = response_data.get("State")
        else:
            state = " "
        if response_data.get("Zip5") != "FALSE":
            z5 = response_data.get("Zip5")
        else:
            z5 = " "
        if response_data.get("Zip4") != "FALSE":
            z4 = response_data.get("Zip4")
        else:
            z4 = " "
        if z4 != " " and z5 != " " and z4 and z5:
            z = z5 + " - " + z4
            ok = "true"
        elif z5:
            z = z5
            ok = "false"
        else:
            raise ValidationError(response_data.get("Error").get("Description"))
        if a2 != " " or a1 != " ":
            am = "true"
        else:
            am = "false"
        cleanse_address_res = {
            "Address2": a1,
            "Address1": a2,
            "City": city,
            "State": state,
            "ZIPCode": z,
            "AddressMatch": am,
            "CityStateZipOK": ok,
        }
        return cleanse_address_res

    def usps_xml_request(self):
        """
        prepare xml data for address validation api
        """
        # Default address as of 6/22: "https://secure.shippingapis.com/ShippingAPI.dll"
        try:
            web = self.env["ir.config_parameter"].sudo().get_param("usps_api_url")
            user_id = self.env["ir.config_parameter"].sudo().get_param("usps_username")
        except Exception:
            raise ValidationError(
                _(
                    "Your credentials are not configured,\
                 please ensure you have a username, password,\
                 and API URL set under Contacts/Configuration/USPS\
                 Credential Configuration"
                )
            )
        address1 = str(self.street)
        address2 = str(self.street2)
        city = str(self.city)
        state = str(self.state_id.code)
        zipcode = str(self.zip)
        request = (
            '%s+?API=Verify&XML=<AddressValidateRequest USERID="%s">\
            <Address ID="0"><Address1>%s</Address1><Address2>%s\
            </Address2><City>%s</City><State>%s</State><Zip5>\
            %s</Zip5><Zip4></Zip4></Address></AddressValidateRequest>'
            % (web, user_id, address1, address2, city, state, zipcode)
        )
        try:
            response = requests.post(request)
            response_data = xmltodict.parse(response.text)
        except Exception as error:
            raise ValidationError(error)
        if response_data.get("Error"):
            raise ValidationError(response_data.get("Error").get("Description"))
        try:
            cleanse_address_res = self.env["res.partner"].cleanse_address(response_data)
            if cleanse_address_res:
                return cleanse_address_res
            else:
                raise ValidationError(_(response_data))
        except Exception as error:
            raise ValidationError(_(error))
