# -*- coding: utf-8 -*-
# Copyright (C) 2014-2015  Grupo ESOC <www.grupoesoc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
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

    @api.multi
    @api.depends("birthdate_date")
    def _birthdate_compute(self):
        """Store a string of the new date in the old field."""
        for partner in self:
            partner.birthdate = partner.birthdate_date

    @api.multi
    def _birthdate_inverse(self):
        """Convert the old Char date to the new Date format."""
        for partner in self:
            try:
                partner.birthdate_date = partner.birthdate
            except ValueError:
                _logger.warn(_(
                    "Could not convert '{0.birthdate}' to date in "
                    "res.partner {0.id} ({0.name}). Skipping."
                ).format(partner))

    @api.model
    def _birthdate_install(self):
        """Export all old birthdates to the new format."""
        self.search([('birthdate', "!=", False)])._inverse_birthdate()
