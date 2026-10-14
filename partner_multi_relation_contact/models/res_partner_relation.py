# Copyright 2026 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartnerRelation(models.Model):

    _inherit = "res.partner.relation"

    contact_partner_id = fields.Many2one(
        comodel_name="res.partner",
        domain=[("type", "=", "other")],
    )
    email_partner_id = fields.Many2one(
        # This field can be used to set the partner to email to, when
        # using the message compose wizard.
        comodel_name="res.partner",
        compute="_compute_email_partner_id",
    )
    allow_contact_partner = fields.Boolean(
        related="type_id.allow_contact_partner",
    )
    email = fields.Char(compute="_compute_email", store=True)
    phone = fields.Char(compute="_compute_phone", store=True)
    function = fields.Char(compute="_compute_function", store=True)

    @api.constrains("contact_partner_id")
    def _check_contact_address(self):
        """Address should only be filled when allowed on type."""
        for this in self:
            if this.contact_partner_id and not this.type_id.allow_contact_partner:
                raise ValidationError(
                    _(
                        "You can not have a contact partner on relations"
                        "  of type %(type)s.",
                        type=this.type_id.display_name,
                    )
                )

    @api.depends(
        "left_partner_id",
        "left_partner_id.email",
        "right_partner_id",
        "right_partner_id.email",
        "contact_partner_id",
        "contact_partner_id.email",
        "type_id",
        "type_id.preferred_contact",
    )
    def _compute_email_partner_id(self):
        for this in self:
            preferred_contact, fallback_contact = this._get_contact_preference()
            this.email_partner_id = (
                this.contact_partner_id.email
                and this.contact_partner_id
                or preferred_contact.email
                and preferred_contact
                or fallback_contact.email
                and fallback_contact
                or False
            )

    @api.depends("email_partner_id")
    def _compute_email(self):
        for this in self:
            this.email = this.email_partner_id.email  # False if no email partner.

    @api.depends(
        "left_partner_id",
        "left_partner_id.phone",
        "right_partner_id",
        "right_partner_id.phone",
        "contact_partner_id",
        "contact_partner_id.phone",
        "type_id",
        "type_id.preferred_contact",
    )
    def _compute_phone(self):
        for this in self:
            preferred_contact, fallback_contact = this._get_contact_preference()
            this.phone = (
                this.contact_partner_id.phone
                or preferred_contact.phone
                or fallback_contact.phone
                or False
            )

    @api.depends(
        "left_partner_id",
        "left_partner_id.function",
        "right_partner_id",
        "right_partner_id.function",
        "contact_partner_id",
        "contact_partner_id.function",
        "type_id",
        "type_id.preferred_contact",
    )
    def _compute_function(self):
        for this in self:
            preferred_contact, fallback_contact = this._get_contact_preference()
            this.function = (
                this.contact_partner_id.function
                or preferred_contact.function
                or fallback_contact.function
                or False
            )

    def _get_contact_preference(self):
        self.ensure_one()
        if self.type_id.preferred_contact == "left_partner":
            return self.left_partner_id, self.right_partner_id
        return self.right_partner_id, self.left_partner_id

    def unlink(self):
        contacts = self.mapped("contact_partner_id")
        contacts.unlink()
        return super().unlink()

    @api.depends("left_partner_id", "right_partner_id", "type_id", "function")
    def _compute_display_name(self):
        """Add function to name if present."""
        result = super()._compute_display_name()
        function_relations = self.filtered("function")
        if function_relations:
            wf = _(" with function ")  # Prevent repeated translation.
            for this in self:
                this.display_name = this.display_name + wf + this.function
        return result

    def action_contact_address(self):
        self.ensure_one()
        form_view = self.env.ref(
            "partner_multi_relation_contact.form_res_partner_contact_address"
        )
        context = self._get_contact_creation_context()
        return {
            "type": "ir.actions.act_window",
            "res_model": "res.partner",
            "name": _("Contact address for %(relation)s", relation=self.display_name),
            "view_mode": "form",
            "views": [(form_view.id, "form")],
            "context": context,
            "target": "top",
        }

    def _get_contact_creation_context(self):
        """Return context for creation of contact partner."""
        self.ensure_one()
        preferred_contact, fallback_contact = self._get_contact_preference()
        context = {
            "default_relation_id": self.id,
            "default_name": self.with_context(
                current_contact_id=preferred_contact.id
            ).display_name,
            "default_type": "other",
            "default_is_company": False,
        }
        context["default_parent_id"] = (
            preferred_contact.id if self.type_id.set_contact_parent else False
        )
        return context
