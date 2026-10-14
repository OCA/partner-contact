# Copyright 2013-2025 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Support connections between partners."""
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.osv.expression import AND, FALSE_LEAF, is_leaf

# Supported operators for _search_relation_<xxxx> functions.
SUPPORTED_OPERATORS = (
    "=",
    "!=",
    "like",
    "not like",
    "ilike",
    "not ilike",
    "in",
    "not in",
)


class ResPartner(models.Model):
    """Extend partner with relations and allow to search for relations
    in various ways.
    """

    # pylint: disable=invalid-name
    # pylint: disable=no-member
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
    relation_all_ids = fields.One2many(
        comodel_name="res.partner.relation",
        compute="_compute_relation_all_ids",
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

    def _compute_relation_all_ids(self):
        """All relations is a combination of left and right relations."""
        for this in self:
            this.relation_all_ids = this.relation_left_ids | this.relation_right_ids

    def _compute_relation_count(self):
        """Combined count for left and right partners."""
        for this in self:
            this.relation_count = len(this.relation_left_ids.filtered("active")) + len(
                this.relation_right_ids.filtered("active")
            )

    @api.model
    def _search_relation_type_id(self, operator, value):
        """Search partners based on their type of relations."""
        self._check_supported_operator(operator)
        return [
            "|",
            ("relation_left_ids.type_id", operator, value),
            ("relation_right_ids.type_id", operator, value),
        ]

    @api.model
    def _check_supported_operator(self, operator):
        """Many search operations only work with comparison operators or (not) in."""
        if operator not in SUPPORTED_OPERATORS:
            raise ValidationError(_('Unsupported search operator "%s"', operator))

    @api.model
    def _search_relation_partner_id(self, operator, value):
        """Find partner based on relation with other partner."""
        # pylint: disable=no-self-use
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
            return [FALSE_LEAF]  # pragma: no cover
        return [
            "|",
            ("relation_left_ids", "in", left_relations.ids),
            ("relation_right_ids", "in", right_relations.ids),
        ]

    @api.model
    def _search_relation_partner_category_id(self, operator, value):
        """Search for partner related to a partner with search category."""
        # pylint: disable=no-self-use
        return [
            "|",
            ("relation_left_ids.right_partner_id.category_id", operator, value),
            ("relation_right_ids.left_partner_id.category_id", operator, value),
        ]

    @api.model
    def search(self, domain, **kwargs):
        """Inject searching for current relation date if we search for
        relation properties and no explicit date was given.
        """
        relation_search = self._get_domain_relation_search(domain)
        if relation_search:
            # Could be inline, but this is easier for unit test.
            domain = self._update_domain_relation_search(domain, relation_search)
        return super().search(domain, **kwargs)

    def _get_domain_relation_search(self, domain):
        """Check whether domain contains elements that search on relations."""
        relation_search = []
        for part in domain:
            if (
                is_leaf(part)
                and isinstance(part[0], str)
                and part[0].startswith("search_relation")
            ):
                relation_search.append(part[0])
        return relation_search

    def _update_domain_relation_search(self, domain, relation_search):
        """Inject, if needed, date and active criteria in search on relations.

        Need to return new domain if modified, as reassigning will leave
        original list argument (domain) unaffected.
        """
        if "search_relation_date" not in relation_search:
            domain = AND(
                [
                    domain,
                    [("search_relation_date", "=", fields.Date.today())],
                ]
            )
        # because of auto_join, we have to do the active test by hand
        if self.env.context.get("active_test", True):
            domain = AND(
                [
                    domain,
                    [
                        "|",
                        ("relation_left_ids.active", "=", True),
                        ("relation_right_ids.active", "=", True),
                    ],
                ]
            )
        return domain

    def get_partner_type(self):
        """Get partner type for relation.
        :return: 'c' for company or 'p' for person
        :rtype: str
        """
        self.ensure_one()
        return "c" if self.is_company else "p"

    @api.constrains("is_company")
    def _check_relation_compatibility(self):
        """If is_company changes, check relations whether this should be allowed."""
        Relation = self.env["res.partner.relation"]
        for this in self:
            contact_type = this.get_partner_type()
            incompatible_relations = Relation.search(
                [
                    "|",
                    "&",
                    ("left_partner_id", "=", this.id),
                    ("type_id.contact_type_left", "not in", (False, contact_type)),
                    "&",
                    ("right_partner_id", "=", this.id),
                    ("type_id.contact_type_right", "not in", (False, contact_type)),
                ],
                limit=1,
            )
            if incompatible_relations:
                raise ValidationError(
                    _("Cannot change type of partner due to incompatible connections.")
                )

    def action_view_relations(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "res.partner.relation",
            "name": _("Connections for current partner"),
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
