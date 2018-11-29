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
        compute="_compute_birthdate",
        inverse="_inverse_birthdate",
        store=True)

    @api.multi
    @api.depends("birthdate_date")
    def _compute_birthdate(self):
        """Store a string of the new date in the old field."""
        for this in self:
            this.birthdate = this.birthdate_date

    @api.multi
    def _inverse_birthdate(self):
        """Convert the old Char date to the new Date format."""
        for this in self:
            try:
                this.birthdate_date = this.birthdate
            except ValueError:
                _logger.warn(
                    _("Could not convert '{0.birthdate}' to date in "
                      "res.partner {0.id} ({0.name}). Skipping.").format(this))
