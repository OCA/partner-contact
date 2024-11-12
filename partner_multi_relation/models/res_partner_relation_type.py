# Copyright 2013-2022 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Define the type of relations that can exist between partners."""

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.osv.expression import AND, OR

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
    contact_type_left = fields.Selection(
        selection="get_partner_types", string="Left partner type"
    )
    contact_type_right = fields.Selection(
        selection="get_partner_types", string="Right partner type"
    )
    partner_category_left = fields.Many2one(
        comodel_name="res.partner.category", string="Left partner category"
    )
    partner_category_right = fields.Many2one(
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
        # pylint: disable=no-self-use
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
        relation_model = self.env["res.partner.relation"]

        def get_type_condition(vals, side):
            """Add if needed check for contact type."""
            fieldname1 = f"contact_type_{side}"
            fieldname2 = f"{side}_partner_id.is_company"
            contact_type = fieldname1 in vals and vals[fieldname1] or False
            if contact_type == "c":
                # Records that are not companies are invalid:
                return [(fieldname2, "=", False)]
            if contact_type == "p":
                # Records that are companies are invalid:
                return [(fieldname2, "=", True)]
            return [(0, "=", 1)]

        def get_category_condition(vals, side):
            """Add if needed check for partner category."""
            fieldname1 = f"partner_category_{side}"
            fieldname2 = f"{side}_partner_id.category_id"
            category_id = fieldname1 in vals and vals[fieldname1] or False
            if category_id:
                # Records that do not have the specified category are invalid:
                return [(fieldname2, "not in", [category_id])]
            return [(0, "=", 1)]

        for this in self:
            handling = (
                "handle_invalid_onchange" in vals
                and vals["handle_invalid_onchange"]
                or this.handle_invalid_onchange
            )
            if handling == "ignore":
                continue
            invalid_conditions = [(0, "=", 1)]
            for side in ["left", "right"]:
                invalid_conditions = OR(
                    [invalid_conditions, get_type_condition(vals, side)]
                )
                invalid_conditions = OR(
                    [invalid_conditions, get_category_condition(vals, side)]
                )
            if not invalid_conditions:
                continue
            # only look at relations for this type
            invalid_domain = AND([[("type_id", "=", this.id)], invalid_conditions])
            invalid_relations = relation_model.with_context(active_test=False).search(
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
                        "type %s. There are existing reflexive "
                        "relations defined for the following partners: "
                        "%s",
                        relation_type.display_name,
                        relations.mapped("left_partner_id.display_name"),
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

        @attention: All fields ending in `_right` will have their values
                    replaced by the values of the fields whose names end
                    in `_left`.
        """
        vals["name_inverse"] = vals.get("name", self.name)
        # For all left keys in model, take value for right either from
        # left key in vals, or if not present, from right key in self:
        left_keys = [key for key in self._fields if key.endswith("_left")]
        for left_key in left_keys:
            right_key = left_key.replace("_left", "_right")
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
        self.env["res.partner.relation"].search(
            [
                (
                    "type_id",
                    "in",
                    self.filtered(
                        lambda rel_type: rel_type.handle_invalid_onchange == "delete"
                    ).ids,
                )
            ],
        ).unlink()
        return super().unlink()
