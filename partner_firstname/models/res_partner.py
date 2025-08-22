# Copyright 2013 Nicolas Bessi (Camptocamp SA)
# Copyright 2014 Agile Business Group (<http://www.agilebg.com>)
# Copyright 2015 Grupo ESOC (<http://www.grupoesoc.es>)
# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    """Adds last name and first name; name becomes a stored function field."""

    _name = "res.partner"
    _inherit = ["res.partner", "firstname.mixin"]

    firstname = fields.Char("First name", index=True)

    lastname = fields.Char("Last name", index=True)

    name = fields.Char(
        compute="_compute_name",
        inverse="_inverse_name_after_cleaning_whitespace",
        required=False,
        store=True,
        readonly=False,
    )

    # @api.depends(lambda self: self._get_fields_depend_firstname_lastname_required())
    def _compute_firstname_lastname_required(self):
        for partner in self.filtered(lambda x: x.is_company or not x.type == "contact"):
            partner.firstname_required = False
            partner.lastname_required = False

        return super(
            ResPartner,
            self.filtered(lambda x: not x.is_company and x.type == "contact"),
        )._compute_firstname_lastname_required()

    def _get_fields_depend_firstname_lastname_required(self):
        res = super()._get_fields_depend_firstname_lastname_required()
        res += ["is_company", "type"]
        return res

    @api.model_create_multi
    def create(self, vals_list):
        """Add inverted names at creation if unavailable. Also, remove the full name
        from `vals` and context if the partner is an individual and is being created
        with any name fields, as the name must be computed from the provided name parts;
        otherwise, the name fields will be computed from the `name` again, when calling
        its inverse method.

        Note that, to avoid deleting the 'default_name' context for all partners when
        it's not appropriate, we must call `create` for each partner individually with
        the correct context.
        """
        created_partners = self.browse()
        for vals in vals_list:
            partner_context = dict(self.env.context)
            is_company = vals.get("company_type") == "company"
            if not is_company and self.name_fields_in_vals(vals) and "name" in vals:
                del vals["name"]
                partner_context.pop("default_name", None)
            else:
                name = vals.get("name", partner_context.get("default_name"))
                if name is not None:
                    # Calculate the split fields
                    inverted = self._get_inverse_name(
                        self._get_whitespace_cleaned_name(name), is_company
                    )
                    for key, value in inverted.items():
                        if not vals.get(key) or partner_context.get("copy"):
                            vals[key] = value

                    # Remove the combined fields
                    vals.pop("name", None)
                    partner_context.pop("default_name", None)
            # pylint: disable=W8121
            created_partners |= super(
                ResPartner, self.with_context(partner_context)
            ).create([vals])
        return created_partners

    def get_extra_default_copy_values(self):
        """Method to add '(copy)' suffix to lastname or firstname, depending on name
        order configuration.
        """
        if self._get_names_order() == "first_last":
            return {
                "lastname": _("%s (copy)", self.lastname)
                if self.lastname
                else _("(copy)")
            }
        return {
            "firstname": _("%s (copy)", self.firstname)
            if self.firstname
            else _("(copy)")
        }

    def copy(self, default=None):
        """Ensure partners are copied right.

        Odoo adds ``(copy)`` to the end of :attr:`~.name`, but that would get
        ignored in :meth:`~.create` because it also copies explicitly firstname
        and lastname fields.
        """
        default = default or {}
        records = self.browse()
        for record in self:
            extra_default_values = record.get_extra_default_copy_values()
            records |= super(ResPartner, record.with_context(copy=True)).copy(
                default | extra_default_values
            )
        return records

    @api.depends("firstname", "lastname")
    def _compute_name(self):
        """Write the 'name' field according to splitted data."""
        for partner in self:
            partner.name = partner._get_computed_name(
                partner.lastname, partner.firstname
            )

    def _inverse_name_after_cleaning_whitespace(self):
        """Clean whitespace in :attr:`~.name` and split it.

        The splitting logic is stored separately in :meth:`~._inverse_name`, so
        submodules can extend that method and get whitespace cleaning for free.
        """
        for record in self:
            # Remove unneeded whitespace
            clean = record._get_whitespace_cleaned_name(record.name)
            record.name = clean
            record._inverse_name()

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
        records._inverse_name()
        _logger.info("%d partners updated installing module.", len(records))

    # Disabling SQL constraint givint a more explicit error using a Python
    # contstraint
    _sql_constraints = [("check_name", "CHECK( 1=1 )", "Contacts require a name.")]
