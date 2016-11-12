# -*- coding: utf-8 -*-
# Copyright (C) 2014-2015  Grupo ESOC <www.grupoesoc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
import logging


_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
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
