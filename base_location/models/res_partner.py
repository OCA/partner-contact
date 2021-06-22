# Copyright 2016 Nicolas Bessi, Camptocamp SA
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    zip_id = fields.Many2one(
        comodel_name="res.city.zip",
        string="ZIP Location",
        index=True,
        compute="_compute_zip_id",
        readonly=False,
        store=True,
        domain="[('city_id', '=?', city_id), "
        "('city_id.country_id', '=?', country_id), "
        "('city_id.state_id', '=?', state_id)]",
    )
    city_id = fields.Many2one(
        index=True,  # add index for performance
        compute="_compute_city_id",
        readonly=False,
        store=True,
    )
    city = fields.Char(compute="_compute_city", readonly=False, store=True)
    zip = fields.Char(compute="_compute_zip", readonly=False, store=True)
    country_id = fields.Many2one(
        compute="_compute_country_id", readonly=False, store=True
    )
    state_id = fields.Many2one(compute="_compute_state_id", readonly=False, store=True)

    @api.depends("state_id", "country_id")
    def _compute_zip_id(self):
        """Empty the zip auto-completion field if data mismatch when on UI."""
        for record in self.filtered("zip_id"):
            for field in ["state_id", "country_id"]:
                if (
                    record[field]
                    and record[field] != record._origin[field]
                    and record[field] != record.zip_id.city_id[field]
                ):
                    record.zip_id = False

    @api.depends("zip_id")
    def _compute_city_id(self):
        if hasattr(super(), "_compute_city_id"):
            super()._compute_city_id()  # pragma: no cover
        for record in self:
            if record.zip_id:
                record.city_id = record.zip_id.city_id
            elif not record.country_enforce_cities:
                record.city_id = False

    @api.depends("zip_id")
    def _compute_city(self):
        if hasattr(super(), "_compute_city"):
            super()._compute_city()  # pragma: no cover
        for record in self:
            if record.zip_id:
                record.city = record.zip_id.city_id.name

    @api.depends("zip_id")
    def _compute_zip(self):
        if hasattr(super(), "_compute_zip"):
            super()._compute_zip()  # pragma: no cover
        for record in self:
            if record.zip_id:
                record.zip = record.zip_id.name

    @api.depends("zip_id", "state_id")
    def _compute_country_id(self):
        if hasattr(super(), "_compute_country_id"):
            super()._compute_country_id()  # pragma: no cover
        for record in self:
            if record.zip_id.city_id.country_id:
                record.country_id = record.zip_id.city_id.country_id
            elif record.state_id:
                record.country_id = record.state_id.country_id

    @api.depends("zip_id")
    def _compute_state_id(self):
        if hasattr(super(), "_compute_state_id"):
            super()._compute_state_id()  # pragma: no cover
        for record in self:
            state = record.zip_id.city_id.state_id
            if state and record.state_id != state:
                record.state_id = record.zip_id.city_id.state_id

    @api.constrains("zip_id", "country_id", "city_id", "state_id")
    def _check_zip(self):
        if self.env.context.get("skip_check_zip"):
            return
        for rec in self:
            if not rec.zip_id:
                continue
            if rec.zip_id.city_id.state_id != rec.state_id:
                raise ValidationError(
                    _("The state of the partner %s differs from that in " "location %s")
                    % (rec.name, rec.zip_id.name)
                )
            if rec.zip_id.city_id.country_id != rec.country_id:
                raise ValidationError(
                    _(
                        "The country of the partner %s differs from that in "
                        "location %s"
                    )
                    % (rec.name, rec.zip_id.name)
                )
            if rec.zip_id.city_id != rec.city_id:
                raise ValidationError(
                    _("The city of partner %s differs from that in " "location %s")
                    % (rec.name, rec.zip_id.name)
                )
