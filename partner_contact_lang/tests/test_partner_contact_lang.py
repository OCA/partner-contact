# Copyright 2016 Tecnativa - Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2017 Tecnativa - Vicent Cubells <vicent.cubells@tecnativa.com>
# Copyright 2018 Tecnativa - Cristina Martín
# Copyright 2021 Pesol - Pedro Evaristo Gonzalez Sanchez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestPartnerContactLang(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestPartnerContactLang, cls).setUpClass()
        cls.ResPartner = cls.env["res.partner"]
        cls.partner = cls.ResPartner.create({"name": "Partner test", "lang": "en_US"})
        cls.contact = cls.ResPartner.create(
            {"name": "Contact test", "lang": False, "parent_id": cls.partner.id}
        )

    def test_onchange_parent_id(self):
        self.contact.parent_id = False
        res = self.contact.onchange_parent_id()
        self.assertIsNone(res)
        self.contact.parent_id = self.partner
        res = self.contact.onchange_parent_id()
        self.assertEqual(self.contact.lang, "en_US")

    def test_write_parent_lang(self):
        """First empty the field for filling it again afterwards to see if
        the contact gets the same value.
        """
        self.contact.lang = False
        self.partner.lang = False
        self.partner.lang = "en_US"
        self.assertEqual(self.contact.lang, "en_US")
