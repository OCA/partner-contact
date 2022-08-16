# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form, common


class TestPartnerCountryLang(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.lang_fr = cls.env.ref("base.lang_fr")
        cls.lang_fr.active = True
        cls.country_fr = cls.env.ref("base.fr")
        cls.country_fr.lang = cls.lang_fr.code
        cls.partner = cls.env["res.partner"].create({"name": "Mr Odoo"})

    def test_partner_onchange(self):
        partner_form = Form(self.partner)
        partner_form.country_id = self.country_fr
        self.assertEqual(partner_form.lang, self.lang_fr.code)

    def test_partner_create(self):
        partner = self.env["res.partner"].create(
            {"name": "Mrs Odoo", "country_id": self.country_fr.id}
        )
        self.assertEqual(partner.lang, self.lang_fr.code)

    def test_partner_write(self):
        self.partner.write({"country_id": self.country_fr.id})
        self.assertEqual(self.partner.lang, self.lang_fr.code)
