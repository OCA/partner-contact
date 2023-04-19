# Copyright (C) 2023 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.partner_firstname import exceptions


class ResPartner(models.Model):
    _inherit = "res.partner"

    middlename = fields.Char("Middle Name")

    @api.model
    def _get_computed_name(self, lastname, firstname, middlename=None):
        """Compute the 'name' field according to splitted data.
        You can override this method to change the order of lastname and
        firstname and middlename the computed name"""
        order = self._get_names_order()
        if order == "last_first_comma":
            names = list()
            if lastname:
                names.append(lastname)
            if names and firstname:
                names[-1] = names[-1] + ","
            if firstname:
                names.append(firstname)
            if middlename:
                names.append(middlename)
            return " ".join(names)
        elif order == "first_last":
            return " ".join(p for p in (firstname, middlename, lastname) if p)
        else:
            return " ".join(p for p in (lastname, firstname, middlename) if p)

    @api.depends("firstname", "lastname", "middlename")
    def _compute_name(self):
        """Write :attr:`~.name` according to splitted data."""
        for partner in self:
            partner.name = self._get_computed_name(
                partner.lastname,
                partner.firstname,
                partner.middlename,
            )

    def _inverse_name(self):
        """Try to revert the effect of :meth:`._compute_name`."""
        self.ensure_one()
        parts = self._get_inverse_name(self.name, self.is_company)
        # Avoid to hit :meth:`~._check_name` with all 3 fields being ``False``
        before, after = {}, {}
        for key, value in parts.items():
            (before if value else after)[key] = value
        if any([before[k] != self[k] for k in list(before.keys())]):
            self.update(before)
        if any([after[k] != self[k] for k in list(after.keys())]):
            self.update(after)

    @api.model
    def _get_inverse_name(self, name, is_company=False):
        """Compute the inverted name.

        - If the partner is a company, save it in the lastname.
        - Otherwise, make a guess.
        """
        result = {
            "firstname": False,
            "lastname": name or False,
            "middlename": False,
        }

        # Company name goes to the lastname
        if not name or is_company:
            return result

        order = self._get_names_order()
        result.update(super()._get_inverse_name(name, is_company))

        if order == "first_last":
            parts = self._split_part("lastname", result)
            if parts:
                result.update({"middlename": parts[0], "lastname": " ".join(parts[1:])})
        elif order == "last_first_comma":
            parts = self._split_part("firstname", result)
            if parts:
                result.update(
                    {"firstname": parts[0], "middlename": " ".join(parts[1:])}
                )
        else:
            parts = self._split_part("firstname", result)
            if parts:
                result.update(
                    {"firstname": parts[-1], "middlename": " ".join(parts[:-1])}
                )
        return result

    def _split_part(self, name_part, name_split):
        """Split a given part of a name.

        :param name_split: The parts of the name
        :type dict

        :param name_part: The part to split
        :type str
        """
        name = name_split.get(name_part, False)
        parts = name.split(" ", 1) if name else []
        if not name or len(parts) < 2:
            return False
        return parts

    @api.constrains("firstname", "lastname", "middlename")
    def _check_name(self):
        """Ensure at least one name is set."""
        try:
            return super()._check_name()
        except exceptions.EmptyNamesError:
            for partner in self:
                if not partner.middlename:
                    raise
