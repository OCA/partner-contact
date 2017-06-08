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

from openerp import api, fields, models
from . import exceptions


class Partner(models.Model):
    _inherit = "res.partner"

    disability_percentage = fields.Integer()

    @api.one
    @api.constrains("disability_percentage")
    def _disability_percentage_check(self):
        """Can only be a value from 0 to 100."""
        if self.disability_percentage:
            if not 0 <= self.disability_percentage <= 100:
                raise exceptions.OutOfRangeError(self)
