# Copyright 2025 Sylvain LE GAL (GRAP)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models

from .. import exceptions


class FirstNameMixin(models.AbstractModel):
    _name = "firstname.mixin"
    _description = (
        "Manage common things needed for models"
        " that have firstname / lastname fields."
    )

    form_has_lastname_first = fields.Boolean(compute="_compute_form_has_lastname_first")

    firstname_required = fields.Boolean(compute="_compute_firstname_lastname_required")

    lastname_required = fields.Boolean(compute="_compute_firstname_lastname_required")

    @api.depends(lambda self: self._get_fields_depend_firstname_lastname_required())
    def _compute_firstname_lastname_required(self):
        required_fields = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("partner_names_required_fields")
        )
        for partner in self:
            partner.firstname_required = not partner.lastname or required_fields in [
                "firstname",
                "firstname_lastname",
            ]
            partner.lastname_required = not partner.firstname or required_fields in [
                "lastname",
                "firstname_lastname",
            ]

    def _compute_form_has_lastname_first(self):
        names_order = self._get_names_order()
        for record in self:
            record.form_has_lastname_first = names_order != "first_last"

    def _get_fields_depend_firstname_lastname_required(self):
        return ["lastname", "firstname"]

    @api.model
    def default_get(self, fields_list):
        """Invert name when getting default values."""
        if (
            "firstname" in fields_list or "lastname" in fields_list
        ) and "name" not in fields_list:
            fields_list.append("name")
        result = super().default_get(fields_list)

        inverted = self._get_inverse_name(
            self._get_whitespace_cleaned_name(result.get("name", "")),
            result.get("is_company", False),
        )

        for field in list(inverted.keys()):
            if field in fields_list:
                result[field] = inverted.get(field)

        return result

    @api.model
    def _get_names_order(self):
        """Get names order configuration from system parameters.
        You can override this method to read configuration from language,
        country, company or other"""
        default_order = (
            self.env["res.config.settings"].sudo()._partner_names_order_default()
        )
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("partner_names_order", default_order)
        )

    @api.model
    def _get_whitespace_cleaned_name(self, name, comma=False):
        """Remove redundant whitespace from :param:`name`.

        Removes leading, trailing and duplicated whitespace.
        """
        if isinstance(name, bytes):
            # With users coming from LDAP, name can be a byte encoded string.
            # This happens with FreeIPA for instance.
            name = name.decode("utf-8")

        try:
            name = " ".join(name.split()) if name else name
        except UnicodeDecodeError:
            # with users coming from LDAP, name can be a str encoded as utf-8
            # this happens with ActiveDirectory for instance, and in that case
            # we get a UnicodeDecodeError during the automatic ASCII -> Unicode
            # conversion that Python does for us.
            # In that case we need to manually decode the string to get a
            # proper unicode string.
            name = " ".join(name.decode("utf-8").split()) if name else name

        if comma:
            name = name.replace(" ,", ",")
            name = name.replace(", ", ",")
        return name

    @api.model
    def _get_computed_name(self, lastname, firstname):
        """Compute the 'name' field according to splitted data.
        You can override this method to change the order of lastname and
        firstname the computed name"""
        order = self._get_names_order()
        if order == "last_first_comma":
            return ", ".join(p for p in (lastname, firstname) if p)
        elif order == "first_last":
            return " ".join(p for p in (firstname, lastname) if p)
        else:
            return " ".join(p for p in (lastname, firstname) if p)

    @api.model
    def _get_inverse_name(self, name, is_company=False):
        """Compute the inverted name.

        - If the partner is a company, save it in the lastname.
        - Otherwise, make a guess.

        This method can be easily overriden by other submodules.
        You can also override this method to change the order of name's
        attributes

        When this method is called, :attr:`~.name` already has unified and
        trimmed whitespace.
        """
        # Company name goes to the lastname
        if is_company or not name:
            parts = [name or False, False]
        # Guess name splitting
        else:
            order = self._get_names_order()
            # Remove redundant spaces
            name = self._get_whitespace_cleaned_name(
                name, comma=(order == "last_first_comma")
            )
            parts = name.split("," if order == "last_first_comma" else " ", 1)
            if len(parts) > 1:
                if order == "first_last":
                    parts = [" ".join(parts[1:]), parts[0]]
                else:
                    parts = [parts[0], " ".join(parts[1:])]
            else:
                while len(parts) < 2:
                    parts.append(False)
        return {"lastname": parts[0], "firstname": parts[1]}

    @api.model
    def name_fields_in_vals(self, vals):
        """Method to check if any name fields are in `vals`."""
        return vals.get("firstname") or vals.get("lastname")

    @api.constrains("name", "firstname", "lastname")
    def _check_name(self):
        """Ensure that name, firstname and lastname are correctly set
        depending on the configuration and on the type of the record."""
        for record in self:
            if any(
                [
                    record.is_company and not record.name,
                    record.firstname_required and not record.firstname,
                    record.lastname_required and not record.lastname,
                ]
            ):
                raise exceptions.EmptyNamesError(record, self.env)
