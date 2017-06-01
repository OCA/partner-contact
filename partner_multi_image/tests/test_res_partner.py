# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.tests.common import TransactionCase
from openerp.modules import get_module_resource


class ResPartnerCase(TransactionCase):
    def setUp(self):
        super(ResPartnerCase, self).setUp()
        self.partner = self.env["res.partner"].create({
            "name": "somebody",
        })

    def tearDown(self):
        """Remove stored images."""
        self.partner.image = False
        return super(ResPartnerCase, self).tearDown()

    def test_set_image(self):
        """Image is OK."""
        path = get_module_resource(
            "partner_multi_image", "static/description", "icon.png")
        with open(path, "rb") as image:
            self.partner.image = image.read().encode("base64")
        self.assertIsNot(self.partner.image, False)
