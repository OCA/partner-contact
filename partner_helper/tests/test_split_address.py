import logging

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestSplit(TransactionCase):
    def setUp(self):
        super(TestSplit, self).setUp()
        self.partnerX = self.env.ref("base.res_partner_12")
        self.partnerX.street = (
            "278 route pitoresque de la vallee de l'ours qui fuit les chasseurs "
            "en courant très très vite"
        )

    def test_split1(self):
        address1, address2 = self.partnerX._get_split_address(2, 40)
        self.assertEqual("278 route pitoresque de la vallee de", address1)
        self.assertEqual("l'ours qui fuit les chasseurs en courant", address2)
        self.assertTrue(len(address1) <= 40)
        self.assertTrue(len(address2) <= 40)

    def test_split2(self):
        address1, address2, address3 = self.partnerX._get_split_address(3, 25)
        self.assertEqual("278 route pitoresque de", address1)
        self.assertEqual("la vallee de l'ours qui", address2)
        self.assertEqual("fuit les chasseurs en", address3)
        self.assertTrue(len(address1) <= 25)
        self.assertTrue(len(address2) <= 25)
        self.assertTrue(len(address3) <= 25)

    def test_split3(self):
        with self.assertRaises(UserError) as e:
            self.partnerX._get_split_address(3, 15, strict=True)
        self.assertEqual(
            e.exception.name,
            "The address is too long following word can not be "
            "processed 'qui fuit les chasseurs en courant très très vite'",
        )
