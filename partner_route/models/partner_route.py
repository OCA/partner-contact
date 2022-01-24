# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class PartnerRoute(models.Model):
    _name = "partner.route"
    _description = "Partner Routes"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible",
        help="Which user is in charge of the route",
    )
    route_type = fields.Selection(
        selection=[
            ("crm", "CRM"),
            ("sale", "Sales"),
            ("delivery", "Delivery"),
            ("repair", "Repair"),
        ],
    )
    interval_unit = fields.Selection(
        string="Interval",
        selection=[
            ("days", "Day(s)"),
            ("weeks", "Week(s)"),
            ("months", "Month(s)"),
            ("years", "Year(s)"),
        ],
        default="weeks",
        required=True,
    )
    recurring_interval = fields.Integer(
        string="Repeat Every",
        required=True,
        default=1,
    )
    next_date = fields.Date(
        string="Next route date",
        compute="_compute_next_date",
        required=True,
        readonly=False,
        store=True,
        default=fields.Date.today(),
    )
    route_day = fields.Boolean(
        string="Applies today",
        compute="_compute_route_day",
        readonly=True,
    )
    route_partner_ids = fields.One2many(
        comodel_name="partner.route.item",
        inverse_name="route_id",
        string="Partners",
    )

    @api.depends("interval_unit", "recurring_interval")
    def _compute_next_date(self):
        if self.next_date == fields.Date.today():
            return
        delta = relativedelta(**{self.interval_unit: self.recurring_interval})
        self.next_date = fields.Date.today() + delta

    @api.depends("next_date")
    def _compute_route_day(self):
        self.route_day = self.next_date == fields.Date.today()


class PartnerRouteItem(models.Model):
    _name = "partner.route.item"
    _description = "Route Partners"
    _order = "sequence, partner_id"

    sequence = fields.Integer()
    route_id = fields.Many2one(
        comodel_name="partner.route",
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
    )
    street = fields.Char(
        related="partner_id.street",
    )
    city = fields.Char(
        related="partner_id.city",
    )
    zip = fields.Char(
        related="partner_id.zip",
    )
    state_id = fields.Many2one(
        related="partner_id.state_id",
    )
    country_id = fields.Many2one(
        related="partner_id.country_id",
    )
