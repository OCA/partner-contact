# Copyright (C) 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests import common


class TestResPartner(common.TransactionCase):
    def setUp(self):
        super(TestResPartner, self).setUp()
        self.dea_category_id = self.env.ref(
            "partner_identification_dea.res_partner_id_category_dea",
            raise_if_not_found=False,
        )
        self.medical_id = self.env.ref(
            "partner_identification_dea.res_partner_id_category_medical",
            raise_if_not_found=False,
        )
        self.date = fields.Date.today() + relativedelta(days=30)
        self.partner_obj = self.env["res.partner"]
        self.partner_number_obj = self.env["res.partner.id_number"]
        self.partner_roy = self.partner_obj.create({"name": "Roy"})
        self.partner_jimmy = self.partner_obj.create({"name": "Jimmy"})
        self.partner_number_obj.create(
            {
                "partner_id": self.partner_roy.id,
                "category_id": self.dea_category_id.id,
                "status": "open",
                "valid_until": self.date,
                "name": "12345600",
            }
        )

        self.partner_number_obj.create(
            {
                "partner_id": self.partner_jimmy.id,
                "category_id": self.medical_id.id,
                "status": "open",
                "valid_until": self.date,
                "name": "12360001",
            }
        )

    def test_send_expiration_date_notification(self):
        self.partner_obj.send_expiration_date_notification()
