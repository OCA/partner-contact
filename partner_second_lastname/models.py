# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

from openerp import api, fields, models
from openerp.addons.partner_firstname import exceptions


class ResPartner(models.Model):
    """Adds a second last name."""

    _inherit = "res.partner"

    lastname2 = fields.Char("Second last name", oldname="lastname_second")

    @api.model
    def _get_computed_name(self, lastname, firstname, lastname2=None):
        """Compute the name combined with the second lastname too.

        We have 2 lastnames, so lastnames and firstname will be separated by a
        comma.
        """
        names = list()

        if lastname:
            names.append(lastname)
        if lastname2:
            names.append(lastname2)
        if names and firstname:
            names[-1] = names[-1] + ","
        if firstname:
            names.append(firstname)

        return u" ".join(names)

    @api.one
    @api.depends("firstname", "lastname", "lastname2")
    def _compute_name(self):
        """Write :attr:`~.name` according to splitted data."""
        self.name = self._get_computed_name(self.lastname,
                                            self.firstname,
                                            self.lastname2)

    @api.one
    def _inverse_name(self):
        """Try to revert the effect of :meth:`._compute_name`."""
        parts = self._get_inverse_name(self.name, self.is_company)

        # Avoid to hit :meth:`~._check_name` with all 3 fields being ``False``
        before, after = dict(), dict()
        for key, value in parts.iteritems():
            (before if value else after)[key] = value
        self.update(before)
        self.update(after)

    @api.model
    def _get_inverse_name(self, name, is_company=False):
        """Compute the inverted name.

        - If the partner is a company, save it in the lastname.
        - Otherwise, make a guess.
        """
        # Company name goes to the lastname
        if is_company or not name:
            parts = [False, name or False, False]

        # The comma separates the firstname
        elif "," in name:
            lastnames, firstname = name.split(",", 1)
            parts = [firstname.strip()] + lastnames.split(" ", 1)

        # Without comma, the user wrote the firstname first
        else:
            parts = name.split(" ", 2)

        while len(parts) < 3:
            parts.append(False)

        return {"firstname": parts[0],
                "lastname": parts[1],
                "lastname2": parts[2]}

    @api.one
    @api.constrains("firstname", "lastname", "lastname2")
    def _check_name(self):
        """Ensure at least one name is set."""
        try:
            super(ResPartner, self)._check_name()
        except exceptions.EmptyNamesError as error:
            if not self.lastname2:
                raise error

    @api.one
    @api.onchange("firstname", "lastname", "lastname2")
    def _onchange_subnames(self):
        """Trigger onchange with :attr:`~.lastname2` too."""
        super(ResPartner, self)._onchange_subnames()
