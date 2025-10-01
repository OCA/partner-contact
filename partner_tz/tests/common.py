# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


class CommonPartnerTz:
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.partner_obj = cls.env["res.partner"]
        cls.partner_utc = cls.partner_obj.create(
            {
                "name": "Partner UTC",
                "tz": "UTC",
            }
        )
        cls.partner_brussels = cls.partner_obj.create(
            {
                "name": "Partner Brussels",
                "tz": "Europe/Brussels",
            }
        )
        cls.partner_new_york = cls.partner_obj.create(
            {
                "name": "Partner New York",
                "tz": "America/New_York",
            }
        )
