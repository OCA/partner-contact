# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models

from odoo.addons.partner_firstname import exceptions


class ResPartner(models.Model):
    """Adds a second last name."""

    _inherit = "res.partner"

    lastname2 = fields.Char(
        "Second last name",
    )

    @api.model
    def name_fields_in_vals(self, vals):
        """Override to check if `lastname2` is in vals."""
        return super().name_fields_in_vals(vals) or vals.get("lastname2")

    def get_extra_default_copy_values(self, default=None):
        """Override to add '(copy)' suffix to lastname2 instead of lastname.

        For formats where lastname2 is the trailing part of the displayed
        name (first_last, last_first_comma2), the copy marker belongs there.
        """
        default = default or {}
        if default.get("name"):
            return self._get_inverse_name(default["name"], self.is_company)
        values = super().get_extra_default_copy_values(default=default)
        order = self._get_names_order()
        if order in ("first_last", "last_first_comma2"):
            if order == "first_last":
                values["lastname"] = default.get("lastname", self.lastname) or ""
            elif order == "last_first_comma2":
                values["firstname"] = default.get("firstname", self.firstname) or ""
            if not default.get("lastname2"):
                values["lastname2"] = (
                    _("%s (copy)", self.lastname2) if self.lastname2 else _("(copy)")
                )
            else:
                values["lastname2"] = default.get("lastname2", self.lastname2) or ""
        else:
            values["lastname2"] = default.get("lastname2", self.lastname2) or ""
        values["name"] = self._get_computed_name(
            values.get("lastname"),
            values.get("firstname"),
            values.get("lastname2"),
        )
        return values

    @api.model
    def _get_computed_name(self, lastname, firstname, lastname2=None):
        """Compute the name combined with the second lastname too.

        We have 2 lastnames, so lastnames and firstname will be separated
        differently depending on the configured name order.
        """
        order = self._get_names_order()
        names = list()
        if order == "first_last":
            if firstname:
                names.append(firstname)
            if lastname:
                names.append(lastname)
            if lastname2:
                names.append(lastname2)
        elif order == "last_first_comma2":
            # Format: "Lastname, Firstname SecondLastname"
            if lastname:
                names.append(lastname)
            if names and (firstname or lastname2):
                names[0] = names[0] + ","
            if firstname:
                names.append(firstname)
            if lastname2:
                names.append(lastname2)
        else:
            if lastname:
                names.append(lastname)
            if lastname2:
                names.append(lastname2)
            if names and firstname and order == "last_first_comma":
                names[-1] = names[-1] + ","
            if firstname:
                names.append(firstname)
        return " ".join(names)

    @api.depends("firstname", "lastname", "lastname2")
    def _compute_name(self):
        """Write :attr:`~.name` according to splitted data."""
        for partner in self:
            partner.name = self._get_computed_name(
                partner.lastname,
                partner.firstname,
                partner.lastname2,
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
            "lastname2": False,
        }

        # Company name goes to the lastname
        if not name or is_company:
            return result

        order = self._get_names_order()

        if order == "last_first_comma2":
            # Expected input: "Lastname, Firstname SecondLastname"
            # Split on comma to isolate the first lastname from the rest.
            clean = self._get_whitespace_cleaned_name(name, comma=True)
            parts = clean.split(",", 1)
            result["lastname"] = parts[0].strip() or False
            if len(parts) > 1:
                rest = parts[1].strip()
                rest_parts = rest.split(" ", 1)
                result["firstname"] = rest_parts[0] or False
                if len(rest_parts) > 1:
                    result["lastname2"] = rest_parts[1] or False
            return result

        result.update(super()._get_inverse_name(name, is_company))

        if order in ("first_last", "last_first_comma"):
            parts = self._split_part("lastname", result)
            if parts:
                result.update({"lastname": parts[0], "lastname2": " ".join(parts[1:])})
        else:
            parts = self._split_part("firstname", result)
            if parts:
                result.update(
                    {"firstname": parts[-1], "lastname2": " ".join(parts[:-1])}
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

    @api.constrains("firstname", "lastname", "lastname2")
    def _check_name(self):
        """Ensure at least one name is set."""
        try:
            return super()._check_name()
        except exceptions.EmptyNamesError:
            for partner in self:
                if not partner.lastname2:
                    raise
