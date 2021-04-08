# Copyright 2013 Nicolas Bessi (Camptocamp SA)
# Copyright 2014 Agile Business Group (<http://www.agilebg.com>)
# Copyright 2015 Grupo ESOC (<http://www.grupoesoc.es>)
# Copyright 2021 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from odoo import api, fields, models

from .. import exceptions

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    """Adds last name and first name; name becomes a stored computed field."""

    _inherit = "res.partner"

    firstname = fields.Char("First name", index=True)
    lastname = fields.Char("Last name", index=True)
    name = fields.Char(
        compute="_compute_name",
        inverse="_inverse_name_after_cleaning_whitespace",
        required=False,
        store=True,
        readonly=False,
    )

    @api.model
    def create(self, vals):
        """Add inverted names at creation if unavailable."""
        context = dict(self.env.context)
        name = vals.get("name", context.get("default_name"))
        if name is not None:
            # Calculate the splitted fields
            inverted = self._get_inverse_name(
                self._get_whitespace_cleaned_name(name),
                vals.get("is_company", self.default_get(["is_company"])["is_company"]),
            )
            for key, value in inverted.items():
                if not vals.get(key) or context.get("copy"):
                    vals[key] = value
            # Remove the combined fields
            if "name" in vals:
                del vals["name"]
            if "default_name" in context:
                del context["default_name"]
        new_record = super(ResPartner, self.with_context(context)).create(vals)
        new_record._check_name()
        return new_record

    def write(self, vals):
        """Check validity of name fields before write."""
        result = super().write(vals)
        self._check_name()
        return result

    def _check_name(self):
        """Ensure at least one name is set.

        No longer a constraint, as this method determines dynamically
        the name fields involved.

        Note that this check is also done, if no name fields were involved in the
        write or create, making this check stricter then in the past.
        """
        if self.env.context.get("no_name_check", False):
            # Name check should not prevent installation of module.
            return
        for record in self:
            record._check_record_name()

    def _check_record_name(self):
        """Check name in a single record."""
        self.ensure_one()
        if self.type in ("invoice", "delivery"):
            return
        if self.is_company:
            if self.name:
                return
        else:
            for fieldname in self._get_firstname_fields() + self._get_lastname_fields():
                if self[fieldname]:
                    return
        raise exceptions.EmptyNamesError(self)

    def copy(self, default=None):
        """Ensure partners are copied right.

        Odoo adds ``(copy)`` to the end of :attr:`~.name`, but that would get
        ignored in :meth:`~.create` because it also copies explicitly firstname
        and lastname fields.
        """
        return super(ResPartner, self.with_context(copy=True)).copy(default)

    @api.model
    def default_get(self, fields_list):
        """Invert name when getting default values."""
        result = super(ResPartner, self).default_get(fields_list)
        inverted = self._get_inverse_name(
            self._get_whitespace_cleaned_name(result.get("name", "")),
            result.get("is_company", False),
        )
        for field in list(inverted.keys()):
            if field in fields_list:
                result[field] = inverted.get(field)
        return result

    @api.model
    def _names_order_default(self):
        return "first_last"

    @api.model
    def _get_names_order(self):
        """Get names order configuration from system parameters.
        You can override this method to read configuration from language,
        country, company or other"""
        context_names_order = self.env.context.get("override_names_order", False)
        if context_names_order:
            return context_names_order
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("partner_names_order", self._names_order_default())
        )

    def _compute_name_depends(self):
        """Determine dynamically the fields that are used to compute the name field."""
        return (
            ["is_company"] + self._get_firstname_fields() + self._get_lastname_fields()
        )

    def _get_firstname_fields(self):
        """Determine dynamically the fields that compose the first name."""
        return ["firstname"]

    def _get_lastname_fields(self):
        """Determine dynamically the fields that compose the last name."""
        return ["lastname"]

    @api.depends(lambda self: self._compute_name_depends())
    def _compute_name(self):
        """Write the 'name' field according to splitted data."""
        order = self._get_names_order()
        # Prevent freshly computed name from being inversed.
        self = self.with_context(no_inverse_name=True)
        for record in self:
            if record.is_company:
                # Keep name and lastname synchronized.
                # Would be more logical to always have empty lastname for
                # company. For the moment keeping this for backward compatibility.
                if not record.name and record.lastname:
                    record.name = record.lastname
                if record.name and not record.lastname:
                    record.lastname = record.name
                continue
            first_names = record._get_first_names()
            last_names = record._get_last_names()
            if order == "last_first_comma":
                record.name = ", ".join(p for p in (last_names, first_names) if p)
            elif order == "first_last":
                record.name = " ".join(p for p in (first_names, last_names) if p)
            else:
                record.name = " ".join(p for p in (last_names, first_names) if p)

    def _get_first_names(self):
        """Get all names that should count as firstname."""
        self.ensure_one()
        return " ".join(
            [(self[fieldname] or "") for fieldname in self._get_firstname_fields()]
        )

    def _get_last_names(self):
        """Get all names that should count as lastname."""
        self.ensure_one()
        return " ".join(
            [(self[fieldname] or "") for fieldname in self._get_lastname_fields()]
        )

    def _inverse_name_after_cleaning_whitespace(self):
        """Clean whitespace in :attr:`~.name` and split it.

        The splitting logic is stored separately in :meth:`~._inverse_name`, so
        submodules can extend that method and get whitespace cleaning for free.
        """
        if self.env.context.get("no_inverse_name", False):
            # Do not inverse just written name.
            return
        for record in self:
            # Remove unneeded whitespace
            clean = record._get_whitespace_cleaned_name(record.name)
            record.name = clean
            record._inverse_name()

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

    def _inverse_name(self):
        """Try to revert the effect of :meth:`._compute_name`."""
        for record in self:
            parts = record._get_inverse_name(record.name, record.is_company)
            record.lastname = parts["lastname"]
            record.firstname = parts["firstname"]

    @api.model
    def _install_partner_firstname(self):
        """Save names correctly in the database.

        Before installing the module, field ``name`` contains all full names.
        When installing it, this method parses those names and saves them
        correctly into the database. This can be called later too if needed.
        """
        # Find records with empty firstname and lastname
        records = self.search([("firstname", "=", False), ("lastname", "=", False)])

        # Force calculations there
        records.with_context(no_name_check=True)._inverse_name()
        _logger.info("%d partners updated installing module.", len(records))

    # Disabling SQL constraint givint a more explicit error using a python check.
    _sql_constraints = [("check_name", "CHECK( 1=1 )", "Contacts require a name.")]
