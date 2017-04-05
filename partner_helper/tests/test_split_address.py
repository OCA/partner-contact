# -*- coding: utf-8 -*-
from openerp.tests.common import TransactionCase
import logging
_logger = logging.getLogger(__name__)


class TestSplit(TransactionCase):

    def setUp(self):
        super(TestSplit, self).setUp()
        self.partnerX = self.env.ref('base.res_partner_12')

    def test_init1(self):
        address = u"278 route pitoresque de la vallee de" \
                  u" l'ours qui fuit les chasseurs"
        partner = self.partnerX
        partner.street = address
        address1, address2 = partner._get_split_address(2, 40)
        self.assertEqual('278 route pitoresque de la vallee de', address1)
        self.assertEqual(u"l'ours qui fuit les chasseurs ", address2)
        self.assertTrue(len(address1) <= 40)
        self.assertTrue(len(address2) <= 40)
