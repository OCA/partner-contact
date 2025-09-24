# Copyright 2013-2025 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Define the type of relations that can exist between partners."""

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.fields import Domain

HANDLE_INVALID_ONCHANGE = [
    (
        "restrict",
        "Do not allow change that will result in invalid relations",
    ),
    (
        "ignore",
        "Allow existing relations that do not fit changed conditions",
    ),
    (
        "end",
        "End relations per today, if they do not fit changed conditions",
    ),
    ("delete", "Delete relations that do not fit changed conditions"),
]


class ResPartnerRelationType(models.Model):
    """Model that defines relation types that might exist between partners"""

    _name = "res.partner.relation.type"
    _description = "Partner Relation Type"
    _order = "name"

    name = fields.Char(required=True, translate=True)
    name_inverse = fields.Char(string="Inverse name", required=True, translate=True)
    left_partner_type = fields.Selection(
        selection="get_partner_types", string="Left partner type"
    )
    right_partner_type = fields.Selection(
        selection="get_partner_types", string="Right partner type"
    )
    left_partner_category_id = fields.Many2one(
        comodel_name="res.partner.category", string="Left partner category"
    )
    right_partner_category_id = fields.Many2one(
        comodel_name="res.partner.category", string="Right partner category"
    )
    allow_self = fields.Boolean(
        string="Reflexive",
        help="This relation can be set up with the same partner left and right",
        default=False,
    )
    is_symmetric = fields.Boolean(
        string="Symmetric",
        help="This relation is the same from right to left as from left to right",
        default=False,
    )
    handle_invalid_onchange = fields.Selection(
        selection=HANDLE_INVALID_ONCHANGE,
        string="Invalid relation handling",
        required=True,
        default="restrict",
        help="When adding relations criteria like partner type and category"
        " are checked.\n"
        "However when you change the criteria, there might be relations"
        " that do not fit the new criteria.\n"
        "Specify how this situation should be handled.",
    )

    @api.model
    def get_partner_types(self):
        """A partner can be an organisation or an individual."""
        return [("c", self.env._("Organisation")), ("p", self.env._("Person"))]

    @api.model
    def _end_active_relations(self, relations):
        """End the relations that are active.

        If a relation is current, that is, if it has a start date
        in the past and end date in the future (or no end date),
        the end date will be set to the current date.

        If a relation has a end date in the past, then it is inactive and
        will not be modified.

        :param relations: a recordset of relations (not necessarily all active)
        """
        today = fields.Date.today()
        relations_to_delete = self.env["res.partner.relation"]
        relations_to_update = self.env["res.partner.relation"]
        for relation in relations:
            if relation.date_start and relation.date_start >= today:
                relations_to_delete += relation
            elif not relation.date_end or relation.date_end > today:
                relations_to_update += relation
        relations_to_delete.unlink()
        relations_to_update.write({"date_end": today})
        self.env.flush_all()

    def check_existing(self, vals):
        """Check wether records exist that do not fit new criteria."""
        Relation = self.env["res.partner.relation"]

        def get_type_condition(vals, side):
            """Add if needed check for contact type."""
            fieldname1 = f"{side}_partner_type"
            contact_type = vals.get(fieldname1, False)
            if not contact_type:
                return None
            # If contact_type is 'p' company records are invalid.
            # If contact_type is 'c' person records are invalid.
            is_company = True if contact_type == "p" else False
            fieldname2 = f"{side}_partner_id.is_company"
            return Domain(fieldname2, "=", is_company)

        def get_category_condition(vals, side):
            """Add if needed check for partner category."""
            fieldname1 = f"{side}_partner_category_id"
            category_id = vals.get(fieldname1, False)
            if not category_id:
                return None
            # Records that do not have the specified category are invalid:
            fieldname2 = f"{side}_partner_id.category_id"
            return Domain(fieldname2, "!=", category_id)

        for this in self:
            handling = (
                "handle_invalid_onchange" in vals
                and vals["handle_invalid_onchange"]
                or this.handle_invalid_onchange
            )
            if handling == "ignore":
                continue
            invalid_conditions = Domain.FALSE
            for side in ["left", "right"]:
                type_condition = get_type_condition(vals, side)
                if type_condition:
                    invalid_conditions |= type_condition
                category_condition = get_category_condition(vals, side)
                if category_condition:
                    invalid_conditions |= category_condition
            if invalid_conditions.is_false():
                continue
            # only look at relations for this type
            invalid_domain = Domain("type_id", "=", this.id) & invalid_conditions
            invalid_relations = Relation.with_context(active_test=False).search(
                invalid_domain
            )
            if invalid_relations:
                if handling == "restrict":
                    raise ValidationError(
                        self.env._(
                            "There are already relations not satisfying the"
                            " conditions for partner type or category."
                        )
                    )
                elif handling == "delete":
                    invalid_relations.unlink()
                else:
                    self._end_active_relations(invalid_relations)

    def _get_reflexive_relations(self):
        """Get all reflexive relations for this relation type.

        :return: a recordset of res.partner.relation.
        """
        self.env.cr.execute(
            """
            SELECT id FROM res_partner_relation
            WHERE left_partner_id = right_partner_id
            AND type_id = %(relation_type_id)s
            """,
            {"relation_type_id": self.id},
        )
        reflexive_relation_ids = [r[0] for r in self.env.cr.fetchall()]
        return self.env["res.partner.relation"].browse(reflexive_relation_ids)

    def _check_no_existing_reflexive_relations(self):
        """Check that no reflexive relation exists for these relation types."""
        for relation_type in self:
            relations = relation_type._get_reflexive_relations()
            if relations:
                raise ValidationError(
                    self.env._(
                        "Reflexivity could not be disabled for the relation "
                        "type %(relation_type)s. There are existing reflexive "
                        "relations defined for the following partners: "
                        "%(partners)s",
                        relation_type=relation_type.display_name,
                        partners=relations.mapped("left_partner_id.display_name"),
                    )
                )

    def _delete_existing_reflexive_relations(self):
        """Delete existing reflexive relations for these relation types."""
        relations_to_delete = self.env["res.partner.relation"]
        for relation_type in self:
            relations = relation_type._get_reflexive_relations()
            relations_to_delete += relations
        relations_to_delete.unlink()

    def _end_active_reflexive_relations(self):
        """End active reflexive relations for these relation types."""
        for relation_type in self:
            reflexive_relations = relation_type._get_reflexive_relations()
            self._end_active_relations(reflexive_relations)

    def _handle_deactivation_of_allow_self(self):
        """Handle the deactivation of reflexivity on these relations types."""
        restrict_relation_types = self.filtered(
            lambda t: t.handle_invalid_onchange == "restrict"
        )
        restrict_relation_types._check_no_existing_reflexive_relations()

        delete_relation_types = self.filtered(
            lambda t: t.handle_invalid_onchange == "delete"
        )
        delete_relation_types._delete_existing_reflexive_relations()

        end_relation_types = self.filtered(lambda t: t.handle_invalid_onchange == "end")
        end_relation_types._end_active_reflexive_relations()

    def _update_right_vals(self, vals):
        """Make sure that on symmetric relations, right vals follow left vals.

        @attention: All fields starting with `_right` will have their values
                    replaced by the values of the fields whose names start
                    with `_left`.
        """
        vals["name_inverse"] = vals.get("name", self.name)
        # For all left keys in model, take value for right either from
        # left key in vals, or if not present, from right key in self:
        left_keys = [key for key in self._fields if key.startswith("left_")]
        for left_key in left_keys:
            right_key = left_key.replace("left_", "right_")
            vals[right_key] = vals.get(left_key, self[left_key])
            if hasattr(vals[right_key], "id"):
                vals[right_key] = vals[right_key].id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("is_symmetric"):
                self._update_right_vals(vals)
        return super().create(vals_list)

    def write(self, vals):
        """Handle existing relations if conditions change."""
        self.check_existing(vals)
        for rec in self:
            rec_vals = vals.copy()
            if rec_vals.get("is_symmetric", rec.is_symmetric):
                self._update_right_vals(rec_vals)
            super(ResPartnerRelationType, rec).write(rec_vals)
        allow_self_disabled = "allow_self" in vals and not vals["allow_self"]
        if allow_self_disabled:
            self._handle_deactivation_of_allow_self()
        return True

    def unlink(self):
        """Allow delete of relation type, even when connections exist.

        Relations can be deleted if relation type allows it, so existing relations do
        not prevent unlink of relation type.
        """
        delete_enabled = self.filtered(lambda r: r.handle_invalid_onchange == "delete")
        if delete_enabled:
            Relation = self.env["res.partner.relation"]
            to_delete = Relation.search([("type_id", "in", delete_enabled.ids)])
            to_delete.unlink()
        return super().unlink()
