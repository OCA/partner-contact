# Copyright 2024 Camptocamp
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestPartnerStorePartner(TransactionCase):
    def test_avatar_path(self):
        partner_id = self.env.ref("base.user_root").partner_id
        partner_id.type = "store"

        self.assertEqual(
            partner_id._avatar_get_placeholder_path(),
            "partner_store/static/img/store.png",
        )
