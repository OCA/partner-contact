# -*- coding: utf-8 -*-

#    Author: Nicolas Bessi. Copyright Camptocamp SA
#    Copyright (C)
#       2014:       Agile Business Group (<http://www.agilebg.com>)
#       2015:       Grupo ESOC <www.grupoesoc.es>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from openerp import api, fields, models
from . import exceptions


class ResPartner(models.Model):
    """Adds last name and first name; name becomes a stored function field."""
    _inherit = 'res.partner'

    firstname = fields.Char("First name")
    lastname = fields.Char("Last name")
    name = fields.Char(
        compute="_name_compute",
        inverse="_name_inverse",
        required=False,
        store=True)

    @api.one
    @api.depends("firstname", "lastname")
    def _name_compute(self):
        """Write the 'name' field according to splitted data."""
        self.name = u" ".join((p for p in (self.lastname,
                                           self.firstname) if p))

    @api.one
    def _name_inverse(self):
        """Try to reverse the effect of :meth:`._name_compute`.

        - If the partner is a company, save it in the lastname.
        - Otherwise, make a guess.
        """
        # Remove unneeded whitespace
        clean = u" ".join(self.name.split(None))

        # Clean name avoiding infinite recursion
        if self.name != clean:
            self.name = clean

        # Save name in the real fields
        else:
            # Company name goes to the lastname
            if self.is_company:
                parts = [clean, False]

            # Guess name splitting
            else:
                parts = clean.split(" ", 1)
                while len(parts) < 2:
                    parts.append(False)

            self.lastname, self.firstname = parts

    @api.one
    @api.constrains("firstname", "lastname")
    def _check_name(self):
        """Ensure at least one name is set."""
        if not (self.firstname or self.lastname):
            raise exceptions.EmptyNamesError(self)

    @api.model
    def _firstname_install(self):
        """Save names correctly in the database.

        Before installing the module, field ``name`` contains all full names.
        When installing it, this method parses those names and saves them
        correctly into the database. This can be called later too if needed.
        """
        # Find records with empty firstname and lastname
        records = self.search([("firstname", "=", False),
                               ("lastname", "=", False)])

        # Force calculations there
        records._name_inverse()
