# -*- encoding: utf-8 -*-

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

from openerp import _, exceptions


class DisabilityError(exceptions.ValidationError):
    def __init__(self, record):
        self.name = _("Error(s) with the disability percentage.")
        self.record = record

    @property
    def value(self):
        raise NotImplementedError()


class OutOfRangeError(DisabilityError):
    @property
    def value(self):
        return (_("Disability %d%% of %s must be between 0 and 100.")
                % (self.record.disability_percentage, self.record))
