# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class ResCompanyLdap(models.Model):

    _inherit = 'res.company.ldap'

    @api.model
    def map_ldap_attributes(self, conf, login, ldap_entry):
        """
        Compose values for a new resource of model res_users,
        based upon the retrieved ldap entry and the LDAP settings.
        :param dict conf: LDAP configuration
        :param login: the new user's login
        :param tuple ldap_entry: single LDAP result (dn, attrs)
        :return: parameters for a new resource of model res_users
        :rtype: dict
        """
        values = super(ResCompanyLdap, self).map_ldap_attributes(
            conf, login, ldap_entry)
        values.update({
            'lastname': ldap_entry[1]['cn'][0],
            'firstname': ldap_entry[1]['givenName'][0],
            'email': ldap_entry[1]['mail'][0],
        })
        return values
