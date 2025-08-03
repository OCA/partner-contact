# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from __future__ import division

from datetime import datetime

from odoo import api, fields, models


class ResPartner(models.Model):
    """Added phonecall details in the partner."""

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
        comodel_name="resource.calendar.attendance",
        string="Aggregated phonecall schedule",
        compute="_compute_phonecall_calendar_ids",
        help="Aggregation of all available phonecall schedules.",
    )

    @api.depends("phonecall_calendar_ids", "phonecall_calendar_attendance_ids")
    def _compute_phonecall_available(self):
        """Know if a partner is available to call right now."""
        Attendance = self.env["resource.calendar.attendance"]
        for one in self:
            domain = [
                ("calendar_id", "in", one.phonecall_calendar_ids.ids)
            ] + one._phonecall_available_domain()
            found = Attendance.search(domain, limit=1)
            one.phonecall_available = bool(found)

    @api.depends("phonecall_calendar_ids")
    def _compute_phonecall_calendar_ids(self):
        """Fill attendance aggregation."""
        for one in self:
            one.phonecall_calendar_attendance_ids = one.mapped(
                "phonecall_calendar_ids.attendance_ids"
            )

    def _search_phonecall_available(self, operator, value):
        """Search quickly if partner is available to call right now."""
        Attendance = self.env["resource.calendar.attendance"]
        available = Attendance.search(self._phonecall_available_domain())
        if operator == "!=" or "not" in operator:
            value = not value
        operator = "in" if value else "not in"
        return [("phonecall_calendar_ids.attendance_ids", operator, available.ids)]

    def _phonecall_available_domain(self):
        """Get a domain to know if we are available to call a partner."""
        now = fields.Datetime.from_string(self.env.context.get("now", datetime.now()))
        date = fields.Date.to_string(now)
        now_tz = fields.Datetime.context_timestamp(self, now)
        float_time = now_tz.hour + ((now_tz.minute / 60) + now_tz.second) / 60
        return [
            ("dayofweek", "=", str(now.weekday())),
            "|",
            ("date_from", "=", False),
            ("date_from", "<=", date),
            "|",
            ("date_to", "=", False),
            ("date_to", ">=", date),
            ("hour_from", "<=", float_time),
            ("hour_to", ">=", float_time),
        ]
