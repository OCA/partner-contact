# Copyright 2013-2025 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Support connections between partners."""

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.fields import Domain
from odoo.tools import OrderedSet


class ResPartner(models.Model):
    """Extend partner with relations and allow to search for relations
    in various ways.
    """

    _inherit = "res.partner"

    relation_left_ids = fields.One2many(
        comodel_name="res.partner.relation",
        inverse_name="left_partner_id",
        string="Left relations with current partner",
        copy=False,
    )
    relation_right_ids = fields.One2many(
        comodel_name="res.partner.relation",
        inverse_name="right_partner_id",
        string="Right relations with current partner",
        copy=False,
    )
    relation_count = fields.Integer(compute="_compute_relation_count")
    search_relation_type_id = fields.Many2one(
        comodel_name="res.partner.relation.type",
        compute=lambda self: self.update({"search_relation_type_id": None}),
        search="_search_relation_type_id",
        string="Has relation of type",
    )
    search_relation_partner_id = fields.Many2one(
        comodel_name="res.partner",
        compute=lambda self: self.update({"search_relation_partner_id": None}),
        search="_search_relation_partner_id",
        string="Has relation with",
    )
    search_relation_date = fields.Date(
        compute=lambda self: self.update({"search_relation_date": None}),
        search="_search_relation_date",
        string="Relation valid",
    )
    search_relation_partner_category_id = fields.Many2one(
        comodel_name="res.partner.category",
        compute=lambda self: self.update({"search_relation_partner_category_id": None}),
        search="_search_relation_partner_category_id",
        string="Has relation with a partner in category",
    )

    def _compute_relation_count(self):
        """Combined count for left and right partners."""
        for this in self:
            this.relation_count = len(this.relation_left_ids.filtered("active")) + len(
                this.relation_right_ids.filtered("active")
            )

    @api.model
    def _search_relation_type_id(self, operator, value):
        """Search partners based on their type of relations."""
        SUPPORTED_OPERATORS = (
            "any",
            "=",
            "!=",
            "like",
            "not like",
            "ilike",
            "not ilike",
            "in",
            "not in",
        )
        if operator not in SUPPORTED_OPERATORS:
            raise ValidationError(
                self.env._('Unsupported search operator "%s"', operator)
            )
        PartnerRelation = self.env["res.partner.relation"]
        left_relations = PartnerRelation.search([("type_id", operator, value)])
        right_relations = PartnerRelation.search([("type_id", operator, value)])
        if not (left_relations or right_relations):
            return Domain.FALSE
        return [
            "|",
            ("relation_left_ids", "in", left_relations.ids),
            ("relation_right_ids", "in", right_relations.ids),
        ]

    @api.model
    def _search_relation_partner_id(self, operator, value):
        """Find partner based on relation with other partner."""
        return [
            "|",
            ("relation_left_ids.right_partner_id", operator, value),
            ("relation_right_ids.left_partner_id", operator, value),
        ]

    @api.model
    def _search_relation_date(self, operator, value):
        """Look only for partners that have a relation valid at date of search.

        This makes only sense when combined with other searches on relations.
        For instance we want to check for partners that had a relation with
        a category of volunteer on 21 february 2022.

        operator is ignored, value must contain a date.
        """
        # For some reason Domain "optimization" morphs date values
        # into an OrderedSet. Undo this, as it will crash later on.
        if isinstance(value, OrderedSet):
            value = list(value)[0]
        PartnerRelation = self.env["res.partner.relation"]
        date_domain = [
            "&",
            "|",
            ("date_start", "=", False),
            ("date_start", "<=", value),
            "|",
            ("date_end", "=", False),
            ("date_end", ">=", value),
        ]
        left_relations = PartnerRelation.search(date_domain)
        right_relations = PartnerRelation.search(date_domain)
        if not (left_relations or right_relations):
            # Can only happen when there are no valid relations at all...
            return Domain.FALSE  # pragma: no cover
        return [
            "|",
            ("relation_left_ids", "in", left_relations.ids),
            ("relation_right_ids", "in", right_relations.ids),
        ]

    @api.model
    def _search_relation_partner_category_id(self, operator, value):
        """Search for partner related to a partner with search category."""
        return [
            "|",
            ("relation_left_ids.right_partner_id.category_id", operator, value),
            ("relation_right_ids.left_partner_id.category_id", operator, value),
        ]

    @api.model
    def search(self, domain, offset=0, limit=None, order=None):
        """Inject searching for current relation date if we search for
        relation properties and no explicit date was given.
        """
        relation_search = self._get_domain_relation_search(domain)
        if relation_search:
            # Could be inline, but this is easier for unit test.
            domain = self._update_domain_relation_search(domain, relation_search)
        return super().search(domain, offset=offset, limit=limit, order=order)

    def _get_domain_relation_search(self, domain):
        """Check whether domain contains elements that search on relations."""
        relation_search = []
        for condition in Domain(domain).iter_conditions():
            # We will only have real conditions in iter_conditions.
            field_name = condition.field_expr
            if field_name.startswith("search_relation"):
                relation_search.append(field_name)
        return relation_search

    def _update_domain_relation_search(self, domain, relation_search):
        """Inject, if needed, date and active criteria in search on relations.

        Need to return new domain if modified, as reassigning will leave
        original list argument (domain) unaffected.
        """
        updated_domain = Domain(domain)  # Make sure we have domain object.
        if "search_relation_date" not in relation_search:
            updated_domain &= Domain("search_relation_date", "=", fields.Date.today())
        # because of bypass_search_access, we have to do the active test by hand
        if self.env.context.get("active_test", True):
            updated_domain &= Domain.OR(
                [
                    Domain("relation_left_ids.active", "=", True),
                    Domain("relation_right_ids.active", "=", True),
                ]
            )
        return updated_domain

    def action_view_relations(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "res.partner.relation",
            "name": self.env._("Connections for current partner"),
            "view_mode": "tree,form",
            # For the moment default views.
            "views": [(False, "list"), (False, "form")],
            "domain": [
                "|",
                ("left_partner_id", "=", self.id),
                ("right_partner_id", "=", self.id),
            ],
            "context": {
                "current_partner_id": self.id,
            },
            "target": "top",
        }
