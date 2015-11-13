# -*- coding: utf-8 -*-
# © <2015> <Paul Catinean>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.addons.website_sale.controllers.main import website_sale


class WebsitePartnerContact(website_sale):

    def _get_mandatory_billing_fields(self):
        """ Remove name from mandatory fields in order to implement first name
        and last name fields that are combined in the end"""
        res = super(
            WebsitePartnerContact, self)._get_mandatory_billing_fields()
        res = [x for x in res if x != 'name']
        res.extend(['firstname', 'lastname'])
        return res

    def _get_mandatory_shipping_fields(self):
        """ Remove name from mandatory fields in order to implement first name
        and last name fields that are combined in the end"""
        res = super(
            WebsitePartnerContact, self)._get_mandatory_shipping_fields()
        res = [x for x in res if x != 'name']
        res.extend(['firstname', 'lastname'])
        return res
