# -*- coding: utf-8 -*-

# Odoo, Open Source Management Solution
# Copyright (C) 2014-2015  Grupo ESOC <www.grupoesoc.es>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from openerp import _, api, fields, models
import logging


_logger = logging.getLogger(__name__)


class Partner(models.Model):
    """Partner with birth date in date format."""
    _inherit = "res.partner"

    # New birthdate field in date format
    birthdate_date = fields.Date("Birthdate")

    # Make the old Char field to reflect the new Date field
    birthdate = fields.Char(
        compute="_birthdate_compute",
        inverse="_birthdate_inverse",
        store=True)

    @api.one
    @api.depends("birthdate_date")
    def _birthdate_compute(self):
        """Store a string of the new date in the old field."""
        self.birthdate = self.birthdate_date

    @api.one
    def _birthdate_inverse(self):
        """Convert the old Char date to the new Date format."""
        try:
            self.birthdate_date = self.birthdate
        except ValueError:
            _logger.warn(
                _("Could not convert '{0.birthdate}' to date in "
                  "res.partner {0.id} ({0.name}). Skipping.").format(self))

    @api.model
    def _birthdate_install(self):
        """Export all old birthdates to the new format."""
        self.search([('birthdate', "!=", False)])._inverse_birthdate()
