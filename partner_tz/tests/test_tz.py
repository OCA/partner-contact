# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import time

from freezegun import freeze_time

from odoo.fields import Datetime
from odoo.tests.common import TransactionCase

from ..tools import (
    tz_to_tz_naive_datetime,
    tz_to_tz_time,
    tz_to_utc_naive_datetime,
    tz_to_utc_time,
    utc_to_tz_naive_datetime,
    utc_to_tz_time,
)
from .common import CommonPartnerTz


class TestPartnerTz(CommonPartnerTz, TransactionCase):
    @freeze_time("2023-02-07 13:00:00")
    def test_naive_from_utc(self):
        # Winter now in Brussels (UTC +1)
        now = Datetime.now()

        tz_now = tz_to_tz_naive_datetime("UTC", self.partner_brussels.tz, now)
        self.assertEqual(Datetime.to_datetime("2023-02-07 14:00:00"), tz_now)

    @freeze_time("2023-02-07 13:00:00")
    def test_naive_from_new_york(self):
        # Winter now in Brussels (UTC +1
        # 13:00:00 + 6 = 19:00:00
        now = Datetime.now()

        tz_now = tz_to_tz_naive_datetime(
            self.partner_new_york.tz, self.partner_brussels.tz, now
        )
        self.assertEqual(Datetime.to_datetime("2023-02-07 19:00:00"), tz_now)

    @freeze_time("2023-02-07 13:00:00")
    def test_naive_to_utc(self):
        # 13:00:00 - 1 = 12:00:00
        now = Datetime.now()
        tz_now = tz_to_utc_naive_datetime(self.partner_brussels.tz, now)
        self.assertEqual(Datetime.to_datetime("2023-02-07 12:00:00"), tz_now)

    @freeze_time("2023-02-07 13:00:00")
    def test_utc_to_naive(self):
        # 13:00:00 + 1 = 14:00:00
        now = Datetime.now()
        tz_now = utc_to_tz_naive_datetime(self.partner_brussels.tz, now)
        self.assertEqual(Datetime.to_datetime("2023-02-07 14:00:00"), tz_now)

    @freeze_time("2023-02-07")
    def test_time_from_new_york(self):
        # Time : 13:00
        # 13:00 + 6 = 19:00
        the_time = time(13, 0)

        tz_time = tz_to_tz_time(
            self.partner_new_york.tz, self.partner_brussels.tz, the_time
        )

        self.assertEqual(time(19, 0), tz_time)

    @freeze_time("2023-02-07")
    def test_time_from_brussels(self):
        # Time : 13:00
        # 13:00 - 6 = 7:00
        the_time = time(13, 0)

        tz_time = tz_to_tz_time(
            self.partner_brussels.tz, self.partner_new_york.tz, the_time
        )

        self.assertEqual(time(7, 0), tz_time)

    @freeze_time("2023-02-07")
    def test_time_to_utc(self):
        # Time : 13:00
        # 13:00 - 6 = 7:00
        the_time = time(13, 0)

        tz_time = tz_to_utc_time(self.partner_brussels.tz, the_time)

        self.assertEqual(time(12, 0), tz_time)

    @freeze_time("2023-02-07")
    def test_utc_to_time(self):
        # Time : 13:00
        # 13:00 + 1 = 14:00
        the_time = time(13, 0)

        tz_time = utc_to_tz_time(self.partner_brussels.tz, the_time)

        self.assertEqual(time(14, 0), tz_time)
