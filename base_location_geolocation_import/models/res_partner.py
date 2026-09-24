# Copyright 2025 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # Change geolocation fields into writable computed fields.
    partner_latitude = fields.Float(
        compute="_compute_geolocation",
        readonly=False,
        store=True,
    )
    partner_longitude = fields.Float(
        compute="_compute_geolocation",
        readonly=False,
        store=True,
    )
    # We do not want to reset manually set geolocation, or geolocation
    # computed from address, that can be more precise then from zip,
    # to be overridden by zip geolocation.
    geolocation_from_zip = fields.Boolean(
        default=False,
        help="Whether geolocation was set from zip_id (on import), or set manually.",
    )

    def write(self, vals):
        """If vals contains partner_latitude but not zip_id, reset from zip."""
        if "partner_latitude" in vals and "zip_id" not in vals:
            vals["geolocation_from_zip"] = False
        return super().write(vals)

    @api.model
    def _update_geolocation_from_zip(self):
        """After import refresh geolocations."""
        partners = self.search(
            [
                ("zip_id", "!=", False),
                "|",
                ("partner_latitude", "in", (False, 0.0)),
                ("geolocation_from_zip", "=", True),
            ]
        ).filtered(lambda r: r.zip_id.latitude != r.partner_latitude)
        partners._compute_geolocation()

    @api.depends("zip_id")
    def _compute_geolocation(self):
        """Set geolocation from zip, unless already set manually."""
        for this in self:
            if this.zip_id and (this.geolocation_from_zip or not this.partner_latitude):
                vals = this._prepare_geolocation_vals()
                this.write(vals)

    def _prepare_geolocation_vals(self):
        """Set values from zip_id."""
        self.ensure_one()
        return {
            "partner_latitude": self.zip_id.latitude,
            "partner_longitude": self.zip_id.longitude,
            "geolocation_from_zip": True,
        }
