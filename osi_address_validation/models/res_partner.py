# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import requests, xmltodict
from odoo import fields, models, _
from odoo.exceptions import ValidationError


class OSIAddressPartner(models.Model):
    _inherit = 'res.partner'

    osi_date_validation = fields.Date(
        "Last Validation Date",
        readonly=True,
        copy=False,
        help="The date the address was last validated by AvaTax and accepted",
    )

    def button_osi_address_validation(self):
        view_ref = self.env.ref("osi_address_validation.osi_address_validation_view_form")
        ctx = self.env.context.copy()
        ctx.update({"active_ids": self.ids, "active_id": self.id})
        return {
            "type": "ir.actions.act_window",
            "name": "OSI Address Validation",
            "binding_view_types": "form",
            "view_mode": "form",
            "view_id": view_ref.id,
            "res_model": "osi.address.validation",
            "nodestroy": True,
            "res_id": False,
            "target": "new",
            "context": ctx,
        }

    def usps_xml_request(self):
        """
        prepare xml data for address validation api
        """
        
        #user_id="619OPENS2125"
        #password="064AB72SN652"
        #web="https://secure.shippingapis.com/ShippingAPI.dll"
        try:
            web = self.env['ir.config_parameter'].sudo().get_param('usps_api_url')
            user_id = self.env['ir.config_parameter'].sudo().get_param('usps_username')
            password = self.env['ir.config_parameter'].sudo().get_param('usps_password')
            print(web)
            print(user_id)
            print(password)
        except:
            raise ValidationError("Your credentials are not configured, please ensure you have a username, password, and API URL set under Contacts/Configuration/USPS Credential Configuration")
		
        address1=str(self.street)
        address2=str(self.street2)
        city=str(self.city)
        state=str(self.state_id.code)
        zip=str(self.zip)

        request='%s+?API=Verify&XML=<AddressValidateRequest USERID="%s"><Address ID="0"><Address1>%s</Address1><Address2>%s</Address2><City>%s</City><State>%s</State><Zip5>%s</Zip5><Zip4></Zip4></Address></AddressValidateRequest>' % (web,user_id,address1,address2,city,state,zip)
        
        try:
            print("INPUT")
            print(request)
            response=requests.post(request)
            response_data=xmltodict.parse(response.text)
            print("OUTPUT")
            print(str(response_data))
        except Exception as error:
            raise ValidationError(error)
        if response_data.get('Error'):
            raise ValidationError(response_data.get('Error').get('Description'))
        try:
            response_data = response_data.get('AddressValidateResponse').get('Address')
            print(response_data)
            if response_data.get('Address1')!="FALSE": a1=response_data.get('Address1')
            else: a1=" "
            if response_data.get('Address2')!="FALSE": a2=response_data.get('Address2')
            else: a2=" "
            if response_data.get('City')!="FALSE": city=response_data.get('City')
            else: city=" "
            if response_data.get('State')!="FALSE": state=response_data.get('State')
            else: state=" "
            if response_data.get('Zip5')!="FALSE": z5=response_data.get('Zip5')
            else: z5=" "
            if response_data.get('Zip4')!="FALSE": z4=response_data.get('Zip4')
            else: z4=" "
            if z4!=" " and z5!=" " and z4 and z5: 
            	z=z5+' - '+z4
            	ok='true'
            elif z5: 
            	z=z5
            	ok='false'
            else:
                raise ValidationError(response_data.get('Error').get('Description'))
            if a2!=" " or a1!=" ": am='true'
            else: am='false'
            
            cleanse_address_res={'Address2':a1,
                                    'Address1':a2,
                                    'City':city,
                                    'State':state,
                                    'ZIPCode':z,
                                    'AddressMatch':am,
                                    'CityStateZipOK':ok,
                                    }
            
            if cleanse_address_res:
                print(cleanse_address_res)
                return cleanse_address_res
            else:
                raise ValidationError(_(response_data))
        except Exception as error:
            raise ValidationError(error)
			

