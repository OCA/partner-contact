# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import mock
from openerp.tests.common import TransactionCase


class TestResCompanyLdap(TransactionCase):

    def setUp(self):
        super(TestResCompanyLdap, self).setUp()
        res_company_ldap_model = self.env['res.company.ldap']
        self.res_company_ldap = res_company_ldap_model.create({
            'company': self.ref('base.main_company'),
            'ldap_server': 'ldap.server.test',
            'ldap_filter': 'uid=%s',
            'ldap_base': 'ou=users,dc=acsone,dc=test',
            'create_user': True,
        })

    def test_user_create_from_ldap_bind(self):
        res_users = self.env['res.users']
        domain = [("firstname", "=", "Laurent"),
                  ("lastname", "=", "Mignon"),
                  ("email", "=", "laurent.mignon@acsone.eu")]
        users = res_users.search(domain)
        self.assertEquals(0, len(users))
        with mock.patch("openerp.addons.auth_ldap.users_ldap.CompanyLDAP."
                        "authenticate") as authenticate:
            authenticate.return_value = (
                'uid=acsone,ou=users,dc=acsone,dc=test',
                {'mailQuotaSize': ['0'],
                 'displayName': ['Acsone Ldap'],
                 'uid': ['acsone'],
                 'objectClass': ['top',
                                 'person',
                                 'organizationalPerson',
                                 'inetOrgPerson',
                                 'posixAccount',
                                 'qmailUser'],
                 'loginShell': ['/sbin/nologin'],
                 'userPassword': ['{SSHA}wyz=='],
                 'uidNumber': ['5153'],
                 'accountStatus': ['active'],
                 'gidNumber': ['5000'],
                 'gecos': ['Acsone Ldap'],
                 'sn': ['Mignon'],
                 'homeDirectory': ['/home/acsonelmi'],
                 'mail': ['laurent.mignon@acsone.eu'],
                 'givenName': ['Laurent'],
                 'cn': ['Mignon']}
            )
            conf = self.res_company_ldap.get_ldap_dicts()[0]
            entry = self.res_company_ldap.authenticate(
                conf, "acsone", "pwd")
            self.assertTrue(entry)
            user_id = self.res_company_ldap.get_or_create_user(
                conf, "acsone", entry)
            self.assertTrue(user_id)
            users = res_users.search(domain)
            self.assertEquals(1, len(users))
            self.assertEquals(user_id, users[0].id)
