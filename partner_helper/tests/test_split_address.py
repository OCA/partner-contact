from odoo.tests.common import TransactionCase
import logging
_logger = logging.getLogger(__name__)


class TestSplit(TransactionCase):

    def setUp(self):
        super(TestSplit, self).setUp()
        self.partnerX = self.env.ref('base.res_partner_12')
        self.partnerX.street = "278 route pitoresque de la vallee de" \
                               " l'ours qui fuit les chasseurs"

    def test_split1(self):
        address1, address2 = self.partnerX._get_split_address(2, 40)
        self.assertEqual('278 route pitoresque de la vallee de', address1)
        self.assertEqual("l'ours qui fuit les chasseurs ", address2)
        self.assertTrue(len(address1) <= 40)
        self.assertTrue(len(address2) <= 40)

    def test_split2(self):
        address1, address2, address3 = self.partnerX._get_split_address(3, 25)
        self.assertEqual('278 route pitoresque de', address1)
        self.assertEqual("la vallee de l'ours qui", address2)
        self.assertEqual("fuit les chasseurs ", address3)
        self.assertTrue(len(address1) <= 25)
        self.assertTrue(len(address2) <= 25)
        self.assertTrue(len(address3) <= 25)
