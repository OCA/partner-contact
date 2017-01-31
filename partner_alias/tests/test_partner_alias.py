# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase

from odoo.exceptions import ValidationError
from psycopg2 import IntegrityError


class TestPartnerAlias(TransactionCase):

    def setUp(self):
        super(TestPartnerAlias, self).setUp()
        self.alias_1 = self.env.ref(
            'partner_alias.res_partner_alias_alias_1'
        )

    def test_check_name(self):
        """ Test raise ValidationError if alias name same as partner """
        with self.assertRaises(ValidationError):
            self.alias_1.firstname = 'Malcom'

    def test_unique_name(self):
        """ Test raises IntegrityError is name not unique """
        with self.assertRaises(IntegrityError):
            self.alias_1.firstname = 'Greg'
