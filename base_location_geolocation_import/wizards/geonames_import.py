# Copyright 2025 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class CityZipGeonamesImport(models.TransientModel):
    _inherit = "city.zip.geonames.import"

    @api.model
    def prepare_zip(self, row, city_id):
        """Add latitude and longitude to zip vals."""
        vals = super().prepare_zip(row, city_id)
        if len(row) > 9:
            vals.update(
                {
                    "latitude": row[9],
                    "longitude": row[10],
                }
            )
        return vals

    def _process_csv(self, parsed_csv, country):
        """Update geolocations after processing."""
        result = super()._process_csv(parsed_csv, country)
        self.env["res.partner"]._update_geolocation_from_zip()
        return result
