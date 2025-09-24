# Copyright 2013-2025 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Store relations (connections) between partners."""

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.fields import Domain


class ResPartnerRelation(models.Model):
    """Model res.partner.relation is used to describe all links or relations
    between partners in the database.

    This model is actually only used to store the data. The model
    res.partner.relation.all, based on a view that contains each record
    two times, once for the normal relation, once for the inverse relation,
    will be used to maintain the data.
    """

    _name = "res.partner.relation"
    _description = "Partner relation"

    left_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Source Partner",
        required=True,
        bypass_search_access=True,
        ondelete="cascade",
    )
    left_partner_id_domain = fields.Binary(
        compute="_compute_left_partner_id_domain",
        default=[],
    )
    right_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Destination Partner",
        required=True,
        bypass_search_access=True,
        ondelete="cascade",
    )
    right_partner_id_domain = fields.Binary(
        compute="_compute_right_partner_id_domain",
        default=[],
    )
    type_id = fields.Many2one(
        comodel_name="res.partner.relation.type",
        string="Type",
        required=True,
        bypass_search_access=True,
    )
    type_id_domain = fields.Binary(
        compute="_compute_type_id_domain",
        default=[],
    )
    date_start = fields.Date("Starting date")
    date_end = fields.Date("Ending date")
    # TODO: Make cron job to auto-archive records with date_end in the past.
    #       Think about what happens when date_end cleared or changed.
    active = fields.Boolean(
        default=True,
        readonly=True,
        help="Records with date_end in the past should be inactive",
    )

    # == Start of fields that depend on context key current_partner_id.
    type_id_display = fields.Char(
        compute="_compute_type_id_display",
        help="In current context relation is inverse",
    )
    this_partner_id = fields.Many2one(
        comodel_name="res.partner",
        compute="_compute_this_partner_id",
        help="Partner shown left when no currently active partner",
    )
    other_partner_id = fields.Many2one(
        comodel_name="res.partner",
        compute="_compute_other_partner_id",
        help="Partner shown right when no currently active partner"
        ", or connected partnes as seen from current partner.",
    )
    # == End of fields that depend on current_partner_id.

    # Start of fields for searching / grouping.
    any_partner_id = fields.Many2many(
        comodel_name="res.partner",
        string="Partner",
        compute=lambda self: self.update({"any_partner_id": None}),
        search="_search_any_partner_id",
    )
    # End of fields for searching / grouping.

    @api.model
    def default_get(self, fields_list):
        result = super().default_get(fields_list)
        if "left_partner_id" in fields_list:
            current_partner = self._get_current_partner()
            if current_partner:
                result["left_partner_id"] = current_partner.id
        return result

    @api.onchange("type_id")
    def _onchange_type_id(self):
        """Unfortunately @api.depends does not work for unsaved changes."""
        self.ensure_one()
        self._compute_left_partner_id_domain()
        self._compute_right_partner_id_domain()
        result = {
            "domain": {
                "left_partner_id": self.left_partner_id_domain,
                "right_partner_id": self.right_partner_id_domain,
            }
        }
        # Check wether domain results in no choice or wrong choice of partners:
        warning = (
            self._check_partner_domain(
                self.left_partner_id, self.left_partner_id_domain, self.env._("left")
            )
            or self._check_partner_domain(
                self.right_partner_id, self.right_partner_id_domain, self.env._("right")
            )
            or {}
        )
        if warning:
            result["warning"] = warning
        return result

    @api.model
    def _check_partner_domain(self, partner, partner_domain, side):
        """Check wether partner_domain results in empty selection
        for partner, or wrong selection of partner already selected.
        """
        test_domain = Domain(partner_domain)
        if partner:
            test_domain &= Domain("id", "=", partner.id)
        Partner = self.env["res.partner"]
        if Partner.search(test_domain, limit=1):
            return None
        message = (
            self.env._("%s partner incompatible with relation type.", side)
            if partner
            else self.env._("No %s partner available for relation type.", side)
        )
        return {
            "title": self.env._("Error!"),
            "message": message,
        }

    @api.onchange("left_partner_id", "right_partner_id")
    def _onchange_partner(self):
        """Unfortunately @api.depends does not work for unsaved changes."""
        self.ensure_one()
        self._compute_type_id_domain()
        result = {
            "domain": {
                "type_id": self.type_id_domain,
            }
        }
        # Check wether domain results in no choice or wrong choice for type_id.
        warning = self._check_type_id_domain()
        if warning:
            result["warning"] = warning
        return result

    def _check_type_id_domain(self):
        """If type_id already selected, check wether it
        is compatible with the computed type_id_domain. An empty
        selection can practically only occur in a practically empty
        database, and will not lead to problems. Therefore not tested.
        """
        self.ensure_one()
        if not self.type_id:
            return None
        test_domain = Domain(self.type_id_domain) & Domain("id", "=", self.type_id.id)
        RelationType = self.env["res.partner.relation.type"]
        if RelationType.search(test_domain, limit=1):
            return None
        return {
            "title": self.env._("Error!"),
            "message": self.env._(
                "Relation type incompatible with selected partner(s)."
            ),
        }

    @api.depends("type_id")
    def _compute_left_partner_id_domain(self):
        """Set domain based mainly on type_id restrictions."""
        for this in self:
            domain = []
            if this.type_id:
                contact_type = this.type_id.left_partner_type
                if contact_type:
                    is_company = True if contact_type == "c" else False
                    domain.append(("is_company", "=", is_company))
                category_id = this.type_id.left_partner_category_id
                if category_id:
                    domain.append(("category_id", "=", category_id.id))
            this.left_partner_id_domain = domain

    @api.depends("type_id")
    def _compute_right_partner_id_domain(self):
        """Set domain based mainly on type_id restrictions."""
        for this in self:
            domain = []
            if this.type_id:
                contact_type = this.type_id.right_partner_type
                if contact_type:
                    is_company = True if contact_type == "c" else False
                    domain.append(("is_company", "=", is_company))
                category_id = this.type_id.right_partner_category_id
                if category_id:
                    domain.append(("category_id", "=", category_id.id))
            this.right_partner_id_domain = domain

    @api.depends("left_partner_id", "right_partner_id")
    def _compute_type_id_domain(self):
        """Set domain based on left and right partner."""
        for this in self:
            domain = []
            left_partner = this.left_partner_id
            if left_partner:
                partner_type = "c" if left_partner.is_company else "p"
                domain += [
                    "|",
                    ("left_partner_type", "=", False),
                    ("left_partner_type", "=", partner_type),
                    "|",
                    ("left_partner_category_id", "=", False),
                    ("left_partner_category_id", "in", left_partner.category_id.ids),
                ]
            right_partner = this.right_partner_id
            if right_partner:
                partner_type = "c" if right_partner.is_company else "p"
                domain += [
                    "|",
                    ("right_partner_type", "=", False),
                    ("right_partner_type", "=", partner_type),
                    "|",
                    ("right_partner_category_id", "=", False),
                    ("right_partner_category_id", "in", right_partner.category_id.ids),
                ]
            this.type_id_domain = domain

    @api.depends(
        "left_partner_id.name",
        "type_id.name",
        "right_partner_id.name",
    )
    @api.depends_context("current_partner_id")
    def _compute_display_name(self):
        """Show inverse names when coming from right partner."""
        current_partner = self._get_current_partner()
        for this in self:
            if this.right_partner_id and this.right_partner_id == current_partner:
                this.display_name = (
                    f"{this.right_partner_id.name or ''}"
                    f" {this.type_id.name_inverse or ''}"
                    f" {this.left_partner_id.name or ''}"
                )
            else:
                this.display_name = (
                    f"{this.left_partner_id.name or ''}"
                    f" {this.type_id.name or ''}"
                    f" {this.right_partner_id.name or ''}"
                )

    @api.depends_context("current_partner_id")
    def _compute_type_id_display(self):
        """Show inverse type when coming from right partner."""
        current_partner = self._get_current_partner()
        for this in self:
            if not this.type_id:
                this.type_id_display = False
                continue
            if this.right_partner_id and this.right_partner_id == current_partner:
                this.type_id_display = this.type_id.name_inverse
                continue
            this.type_id_display = this.type_id.name

    @api.depends_context("current_partner_id")
    def _compute_this_partner_id(self):
        """Show inverse type when coming from right partner."""
        current_partner = self._get_current_partner()
        for this in self:
            this.this_partner_id = (
                this.right_partner_id
                if this.right_partner_id == current_partner
                else this.left_partner_id
            )

    @api.depends_context("current_partner_id")
    def _compute_other_partner_id(self):
        """Show inverse type when coming from right partner."""
        current_partner = self._get_current_partner()
        for this in self:
            this.other_partner_id = (
                this.left_partner_id
                if this.right_partner_id == current_partner
                else this.right_partner_id
            )

    @api.model
    def _get_current_partner(self):
        context = self.env.context
        partner_id = (
            context.get("current_partner_id", False)
            or (
                context.get("active_model") == "res.partner"
                and context.get("active_id", False)
            )
            or False
        )
        PartnerModel = self.env["res.partner"]
        return PartnerModel.browse(partner_id) if partner_id else PartnerModel

    @api.model
    def _search_any_partner_id(self, operator, value):
        """Search relation with partner, no matter on which side."""
        return [
            "|",
            ("left_partner_id", operator, value),
            ("right_partner_id", operator, value),
        ]

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to correct values, before being stored."""
        active_id = self.env.context.get("active_id")
        for vals in vals_list:
            if "left_partner_id" not in vals and active_id:
                vals["left_partner_id"] = active_id
        return super().create(vals_list)

    @api.constrains("date_start", "date_end")
    def _check_dates(self):
        """End date should not be before start date, if not filled

        :raises ValidationError: When constraint is violated
        """
        for record in self:
            if (
                record.date_start
                and record.date_end
                and record.date_start > record.date_end
            ):
                raise ValidationError(
                    self.env._("The starting date cannot be after the ending date.")
                )

    @api.constrains("left_partner_id", "type_id")
    def _check_partner_left(self):
        """Check left partner for required company or person

        :raises ValidationError: When constraint is violated
        """
        self._check_partner("left")

    @api.constrains("right_partner_id", "type_id")
    def _check_partner_right(self):
        """Check right partner for required company or person

        :raises ValidationError: When constraint is violated
        """
        self._check_partner("right")

    def _check_partner(self, side):
        """Check partner for required company or person, and for category

        :param str side: left or right
        :raises ValidationError: When constraint is violated
        """
        for record in self:
            assert side in ["left", "right"]  # pragma no cover
            ptype = getattr(record.type_id, f"{side}_partner_type")
            partner = getattr(record, f"{side}_partner_id")
            if (ptype == "c" and not partner.is_company) or (
                ptype == "p" and partner.is_company
            ):
                raise ValidationError(
                    self.env._(
                        "The %s partner is not applicable for this relation type.", side
                    )
                )
            category = getattr(record.type_id, f"{side}_partner_category_id")
            if category and category.id not in partner.category_id.ids:
                raise ValidationError(
                    self.env._(
                        "The %(side)s partner does not have category %(category)s.",
                        side=side,
                        category=category.name,
                    )
                )

    @api.constrains("left_partner_id", "right_partner_id")
    def _check_not_with_self(self):
        """Not allowed to link partner to same partner

        :raises ValidationError: When constraint is violated
        """
        for record in self:
            if record.left_partner_id == record.right_partner_id:
                if not (record.type_id and record.type_id.allow_self):
                    raise ValidationError(
                        self.env._("Partners cannot have a relation with themselves.")
                    )

    @api.constrains(
        "left_partner_id", "type_id", "right_partner_id", "date_start", "date_end"
    )
    def _check_relation_uniqueness(self):
        """Forbid multiple active relations of the same type between the same
        partners

        :raises ValidationError: When constraint is violated
        """
        for record in self:
            domain = [
                ("type_id", "=", record.type_id.id),
                ("id", "!=", record.id),
                ("left_partner_id", "=", record.left_partner_id.id),
                ("right_partner_id", "=", record.right_partner_id.id),
            ]
            if record.date_start:
                domain += [
                    "|",
                    ("date_end", "=", False),
                    ("date_end", ">=", record.date_start),
                ]
            if record.date_end:
                domain += [
                    "|",
                    ("date_start", "=", False),
                    ("date_start", "<=", record.date_end),
                ]
            if record.search(domain):
                raise ValidationError(
                    self.env._(
                        "There is already a similar relation with overlapping dates"
                    )
                )
