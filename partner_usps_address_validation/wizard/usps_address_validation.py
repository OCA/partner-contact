# Copyright 2022 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class USPSAdressValidation(models.TransientModel):
    _name = "usps.address.validation"
    _description = "USPS Address Validation"

    original_street = fields.Char("Original Street", readonly=True)
    original_street2 = fields.Char("Original Street2", readonly=True)
    original_city = fields.Char("Original City", readonly=True)
    original_zip = fields.Char("Original Zip", readonly=True)
    original_state = fields.Char("Original State", readonly=True)
    original_country = fields.Char("Original Country", readonly=True)
    street = fields.Char("Street")
    street2 = fields.Char("Street2")
    city = fields.Char("City")
    zip = fields.Char("Zip")
    state = fields.Char("State")
    country = fields.Char("Country")
    address_match = fields.Boolean(string="Address Match", readonly="1")
    city_state_zip_match = fields.Boolean(string="City State Zip Match", readonly="1")
    address_result = fields.Char(string="Address Result")

    @api.model
    def default_get(self, fields_list):
        res = super(USPSAdressValidation, self).default_get(fields_list)
        active_id = self.env.context.get("active_id")
        if active_id:
            partner_obj = self.env["res.partner"].browse(active_id)
            res.update(
                {
                    "original_street": partner_obj.street or " ",
                    "original_street2": partner_obj.street2 or " ",
                    "original_city": partner_obj.city or " ",
                    "original_zip": partner_obj.zip or " ",
                    "original_state": partner_obj.state_id
                    and partner_obj.state_id.code
                    or " ",
                    "original_country": partner_obj.country_id
                    and partner_obj.country_id.name
                    or " ",
                }
            )
            valid_address = partner_obj.usps_xml_request()
            res = self.set_valid_address(res, valid_address)
            return res

    def set_valid_address(self, res, valid_address):
        """
        :param: partner_obj res partner object
        """
        address_match = valid_address and valid_address.get("AddressMatch")
        city_state_zip_match = valid_address and valid_address.get("CityStateZipOK")
        address_dict = valid_address
        if address_dict:
            res.update(
                {
                    "street": address_dict and address_dict.get("Address1") or " ",
                    "street2": ""
                    if address_dict.get("Address2") == "FALSE"
                    else address_dict.get("Address2"),
                    "city": address_dict and address_dict.get("City") or " ",
                    "state": address_dict and address_dict.get("State") or " ",
                    "zip": address_dict and address_dict.get("ZIPCode") or " ",
                    "address_result": valid_address.get("AddressCleansingResult")
                    or " ",
                }
            )
            if address_match == "true":
                res.update({"address_match": True})
            if city_state_zip_match == "true":
                res.update({"city_state_zip_match": True})
        return res

    def accept_validate_address(self):
        active_id = self.env.context.get("active_id")
        if active_id:
            address = self.env["res.partner"].browse(active_id)
            state_id = self.env["res.country.state"].search(
                [
                    ("code", "=", self.state),
                    (
                        "country_id",
                        "=",
                        address.country_id
                        and address.country_id.id
                        or self.env.ref("base.us").id,
                    ),
                ]
            )
            vals = {
                "street": self.street,
                "street2": self.street2,
                "city": self.city,
                "zip": self.zip,
                "state_id": state_id and state_id.id or False,
                "usps_date_validation": fields.Date.today(),
            }
            address.write(vals)
        return {"type": "ir.actions.act_window_close"}
