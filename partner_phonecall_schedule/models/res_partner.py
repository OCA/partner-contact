# -*- coding: utf-8 -*-
# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from __future__ import division
from datetime import datetime
from pytz import timezone
from openerp import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    phonecall_available = fields.Boolean(
        "Available to call",
        compute="_compute_phonecall_available",
        search="_search_phonecall_available",
        help="Is it now a good time to call this partner?",
    )
    phonecall_calendar_ids = fields.Many2many(
        comodel_name="resource.calendar",
        string="Phonecall schedule",
        help="Best schedule when the contact expects to be called.",
    )
    phonecall_calendar_attendance_ids = fields.One2many(
        string="Aggregated phonecall schedule",
        related="phonecall_calendar_ids.attendance_ids",
        readonly=True,
    )

    def _compute_phonecall_available(self):
        """Know if a partner is available to call right now."""
        for one in self:
            domain = [
                ("id", "in", one.phonecall_calendar_attendance_ids.ids)
            ] + one._phonecall_available_domain()
            found = one.phonecall_calendar_attendance_ids.search(
                domain, limit=1)
            one.phonecall_available = bool(found)

    def _search_phonecall_available(self, operator, value):
        """Search quickly if partner is available to call right now."""
        Attendance = self.env["resource.calendar.attendance"]
        available = Attendance.search(
            self._phonecall_available_domain(),
        )
        if operator == "!=" or "not" in operator:
            value = not value
        operator = "in" if value else "not in"
        return [("phonecall_calendar_attendance_ids", operator, available.ids)]

    def _phonecall_available_domain(self):
        """Get a domain to know if we are available to call a partner."""
        try:
            tz = timezone(self.env.context["tz"])
        except KeyError:
            tz = None
        now = datetime.now(tz=tz)
        date = now.date()
        float_time = now.hour + ((now.minute / 60) + now.second) / 60
        return [
            ("dayofweek", "=", str(now.weekday())),
            "|", ("date_from", "=", False), ("date_from", "<=", date),
            "|", ("date_to", "=", False), ("date_to", ">=", date),
            ("hour_from", "<=", float_time),
            ("hour_to", ">=", float_time),
        ]
