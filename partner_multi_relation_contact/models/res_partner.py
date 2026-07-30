# Copyright 2026 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    """Enable searching partner via email"""

    _inherit = "res.partner"

    relation_id = fields.Many2one(
        comodel_name="res.partner.relation",
        readonly=True,
        help="Relation for which this contact address has been created",
    )
    allow_contact_partner = fields.Boolean(
        related="relation_id.type_id.allow_contact_partner",
    )
    allow_address = fields.Boolean(
        related="relation_id.type_id.allow_address",
    )
    allow_email = fields.Boolean(
        related="relation_id.type_id.allow_email",
    )
    allow_phone = fields.Boolean(
        related="relation_id.type_id.allow_phone",
    )
    allow_function = fields.Boolean(
        related="relation_id.type_id.allow_function",
    )
    search_relation_email = fields.Many2one(
        comodel_name="res.partner.relation",
        compute=lambda self: self.update({"search_relation_email": None}),
        search="_search_relation_email",
        string="Has relation email",
    )
    search_relation_phone = fields.Many2one(
        comodel_name="res.partner.relation",
        compute=lambda self: self.update({"search_relation_phone": None}),
        search="_search_relation_phone",
        string="Has relation phone",
    )
    search_relation_function = fields.Many2one(
        comodel_name="res.partner.relation",
        compute=lambda self: self.update({"search_relation_function": None}),
        search="_search_relation_function",
        string="Has relation function",
    )

    @api.model_create_multi
    def create(self, vals_list):
        result = super().create(vals_list)
        for record in result:
            if record.relation_id:
                record.relation_id.contact_partner_id = record
        return result

    @api.model
    def _search_relation_email(self, operator, value):
        """Search partners based on their relation email."""
        self._check_supported_operator(operator)
        return [
            "|",
            ("relation_left_ids.contact_partner_id.email", operator, value),
            ("relation_right_ids.contact_partner_id.email", operator, value),
        ]

    @api.model
    def _search_relation_phone(self, operator, value):
        """Search partners based on their relation phone."""
        self._check_supported_operator(operator)
        return [
            "|",
            ("relation_left_ids.contact_partner_id.phone", operator, value),
            ("relation_right_ids.contact_partner_id.phone", operator, value),
        ]

    @api.model
    def _search_relation_function(self, operator, value):
        """Search partners based on their relation function."""
        self._check_supported_operator(operator)
        return [
            "|",
            ("relation_left_ids.contact_partner_id.function", operator, value),
            ("relation_right_ids.contact_partner_id.function", operator, value),
        ]
