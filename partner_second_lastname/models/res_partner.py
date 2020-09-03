# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2017 Tecnativa - Pedro M. Baeza

from odoo import api, fields, models
from odoo.addons.partner_firstname import exceptions


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
        order = self._get_names_order()
        names = list()
        if order == 'first_last':
            if firstname:
                names.append(firstname)
            if lastname:
                names.append(lastname)
            if lastname2:
                names.append(lastname2)
        else:
            if lastname:
                names.append(lastname)
            if lastname2:
                names.append(lastname2)
            if names and firstname and order == 'last_first_comma':
                names[-1] = names[-1] + ","
            if firstname:
                names.append(firstname)
        return u" ".join(names)

    @api.depends("firstname", "lastname", "lastname2")
    def _compute_name(self):
        """Write :attr:`~.name` according to splitted data."""
        for partner in self:
            partner.name = self._get_computed_name(
                partner.lastname, partner.firstname, partner.lastname2,
            )

    @api.one
    def _inverse_name(self):
        """Try to revert the effect of :meth:`._compute_name`."""
        parts = self._get_inverse_name(self.name, self.is_company)
        # Avoid to hit :meth:`~._check_name` with all 3 fields being ``False``
        before, after = {}, {}
        for key, value in parts.iteritems():
            (before if value else after)[key] = value
        if any([before[k] != self[k] for k in before.keys()]):
            self.update(before)
        if any([after[k] != self[k] for k in after.keys()]):
            self.update(after)

    @api.model
    def _get_inverse_name(self, name, is_company=False):
        """Compute the inverted name.

        - If the partner is a company, save it in the lastname.
        - Otherwise, make a guess.
        """
        # Company name goes to the lastname
        result = {
            'firstname': False,
            'lastname': name or False,
            'lastname2': False,
        }
        if not is_company and name:
            order = self._get_names_order()
            result = super(ResPartner, self)._get_inverse_name(
                name, is_company)
            parts = []
            if order == 'last_first':
                if result['firstname']:
                    parts = result['firstname'].split(" ", 1)
                while len(parts) < 2:
                    parts.append(False)
                result['firstname'] = parts[0]
                result['lastname2'] = parts[1]
            else:
                if result['lastname']:
                    parts = result['lastname'].split(" ", 1)
                while len(parts) < 2:
                    parts.append(False)
                result['lastname'] = parts[0]
                result['lastname2'] = parts[1]
        return result

    @api.constrains("firstname", "lastname", "lastname2")
    def _check_name(self):
        """Ensure at least one name is set."""
        try:
            super(ResPartner, self)._check_name()
        except exceptions.EmptyNamesError:
            for partner in self:
                if not partner.lastname2:
                    raise

    @api.onchange("firstname", "lastname", "lastname2")
    def _onchange_subnames(self):
        """Trigger onchange with :attr:`~.lastname2` too."""
        super(ResPartner, self)._onchange_subnames()
