# Copyright 2013-2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# pylint: disable=api-one-deprecated
"""Store relations (connections) between partners."""
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


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
        auto_join=True,
        ondelete="cascade",
    )
    right_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Destination Partner",
        required=True,
        auto_join=True,
        ondelete="cascade",
    )
    type_id = fields.Many2one(
        comodel_name="res.partner.relation.type",
        string="Type",
        required=True,
        auto_join=True,
    )
    date_start = fields.Date("Starting date")
    date_end = fields.Date("Ending date")

    @api.model
    def create(self, vals):
        """Override create to correct values, before being stored."""
        context = self.env.context
        if "left_partner_id" not in vals and context.get("active_id"):
            vals["left_partner_id"] = context.get("active_id")
        return super(ResPartnerRelation, self).create(vals)

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
                    _("The starting date cannot be after the ending date.")
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
            assert side in ["left", "right"]
            ptype = getattr(record.type_id, "contact_type_%s" % side)
            partner = getattr(record, "%s_partner_id" % side)
            if (ptype == "c" and not partner.is_company) or (
                ptype == "p" and partner.is_company
            ):
                raise ValidationError(
                    _("The %s partner is not applicable for this " "relation type.")
                    % side
                )
            category = getattr(record.type_id, "partner_category_%s" % side)
            if category and category.id not in partner.category_id.ids:
                raise ValidationError(
                    _(
                        "The {partner} partner does not have category {category}."
                    ).format(partner=side, category=category.name)
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
                        _("Partners cannot have a relation with themselves.")
                    )

    @api.constrains(
        "left_partner_id", "type_id", "right_partner_id", "date_start", "date_end"
    )
    def _check_relation_uniqueness(self):
        """Forbid multiple active relations of the same type between the same
        partners

        :raises ValidationError: When constraint is violated
        """
        # pylint: disable=no-member
        # pylint: disable=no-value-for-parameter
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
                    _("There is already a similar relation with " "overlapping dates")
                )
