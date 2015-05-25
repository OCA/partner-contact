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

from openerp import api, fields, models
from openerp.addons.partner_firstname import exceptions


class ResPartner(models.Model):
    """Adds a second last name."""

    _inherit = 'res.partner'

    lastname2 = fields.Char("Second last name")

    @api.one
    @api.depends("firstname", "lastname", "lastname2")
    def _name_compute(self):
        """Write the 'name' field according to splitted data.

        We have 2 lastnames, so lastnames and firstname will be separated by a
        comma.
        """

        names = list()

        if self.lastname:
            names.append(self.lastname)
        if self.lastname2:
            names.append(self.lastname2)
        if names and self.firstname:
            names[-1] = names[-1] + ","
        if self.firstname:
            names.append(self.firstname)

        self.name = " ".join(names)

    @api.one
    def _name_inverse(self):
        """Try to revert the effect of :meth:`._name_compute`.

        - If the partner is a company, save it in the lastname.
        - Otherwise, make a guess.
        """
        # Company name goes to the lastname
        if self.is_company:
            parts = [False, self.name, False]

        # The comma separates the firstname
        elif "," in self.name:
            lastnames, firstname = self.name.split(",", 1)
            parts = [firstname.strip()] + lastnames.split(" ", 1)

        # Without comma, the user wrote the firstname first
        else:
            parts = self.name.split(" ", 2)

        while len(parts) < 3:
            parts.append(False)

        # Use old-api `write` to avoid conflicts with :meth:`._check_name`
        self.write({"firstname": parts[0],
                    "lastname": parts[1],
                    "lastname2": parts[2]})

    @api.one
    @api.constrains("firstname", "lastname", "lastname2")
    def _check_name(self):
        """Ensure at least one name is set."""

        try:
            super(ResPartner, self)._check_name()
        except exceptions.EmptyNames as error:
            if not self.lastname2:
                raise error
