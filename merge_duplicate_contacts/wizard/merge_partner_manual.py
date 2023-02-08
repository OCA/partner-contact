import itertools
import logging
import operator
from ast import literal_eval

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class MergePartnerManualCheck(models.TransientModel):
    _name = "merge.partner.manual.check"
    _description = "Merge Partner Manual Check"

    contact_type = fields.Selection(
        [
            ("contact", "Contact"),
            ("invoice", "Invoice address"),
            ("delivery", "Shipping address"),
            ("other", "Other address"),
            ("private", "Private Address"),
        ],
        string="Address Type",
        help="Used by Sales and Purchase Apps to select "
        "the relevant address depending on the context.",
    )

    contact_type2 = fields.Selection(
        [
            ("contact", "Contact"),
            ("invoice", "Invoice address"),
            ("delivery", "Shipping address"),
            ("other", "Other address"),
            ("private", "Private Address"),
        ],
        string="Address Type 2",
        help="Used by Sales and Purchase Apps to select"
        " the relevant address depending on the context.",
    )

    last_changes_date1 = fields.Datetime("Last Changes")
    last_changes_date2 = fields.Datetime("Last Changes 2")

    last_changes_uid1 = fields.Many2one("res.users", "Last Update By")
    last_changes_uid2 = fields.Many2one("res.users", "Last Update By 2")

    last_order1 = fields.Datetime("Last Order")
    last_order2 = fields.Datetime("Last Order 2")

    last_order_num1 = fields.Char("Last Order Number")
    last_order_num2 = fields.Char("Last Order Number 2")

    id1 = fields.Char("ID 1")
    id2 = fields.Char("ID 2")

    partner_id_1 = fields.Many2one("res.partner", "Partner")
    partner_id_2 = fields.Many2one("res.partner", "Partner 2")

    company_id = fields.Many2one("res.partner", "Company")
    company_id2 = fields.Many2one("res.partner", "Company 2")

    company_name = fields.Char()
    company_name2 = fields.Char(string="Company Name 2")

    name = fields.Char()
    name2 = fields.Char("Name 2")

    email = fields.Char()
    email2 = fields.Char("Email 2")

    phone = fields.Char()
    phone2 = fields.Char("Phone 2")

    mobile = fields.Char()
    mobile2 = fields.Char("Mobile 2")

    street = fields.Char("Address1")
    street2 = fields.Char("Address1 2")

    street11 = fields.Char("Address2")
    street22 = fields.Char("Address2 2")

    zip = fields.Char()
    zip2 = fields.Char("Zip 2")

    city = fields.Char()
    city2 = fields.Char("City 2")

    state_id = fields.Many2one("res.country.state", string="State")
    state_id2 = fields.Many2one("res.country.state", string="State 2")

    country_id = fields.Many2one("res.country", string="Country")
    country_id2 = fields.Many2one("res.country", string="Country 2")

    is_company = fields.Boolean("Is Company ?")
    is_company2 = fields.Boolean("Is Company 2 ?")

    vat_1 = fields.Char("Vat")
    vat_2 = fields.Char()

    keep1 = fields.Boolean("Keep", default=True)
    keep2 = fields.Boolean("Keep 2")

    partner_wizard_id = fields.Many2one("base.partner.merge.automatic.wizard", "Wizard")
    partner_ids = fields.Many2many(
        "res.partner",
        "partner_merge_manual_check_rel",
        "marge_id",
        "partner_id",
        string="Contacts",
    )

    current_line_id = fields.Many2one("base.partner.merge.line", string="Current Line")
    dst_partner_id = fields.Many2one("res.partner", string="Destination Contact")

    state = fields.Selection(
        [("option", "Option"), ("selection", "Selection"), ("finished", "Finished")],
        readonly=True,
        required=True,
        string="Status",
        default="option",
    )

    line_ids = fields.One2many("base.partner.merge.line", "wizard_id", string="Lines")
    number_group = fields.Integer("Group of Contacts", readonly=True)
    total_duplicates = fields.Integer()
    duplicate_position = fields.Integer("Duplicate Contact Position")

    name_show_icon = fields.Boolean(
        "Name Icon", compute="_compute_name_show_icon", store=True
    )
    company_show_icon = fields.Boolean(
        "Company Icon", compute="_compute_company_show_icon", store=True
    )
    company_name_show_icon = fields.Boolean(
        "Company Name Icon", compute="_compute_company_name_show_icon", store=True
    )
    email_show_icon = fields.Boolean(
        "Email Icon", compute="_compute_email_show_icon", store=True
    )
    phone_show_icon = fields.Boolean(
        "Phone Icon", compute="_compute_phone_show_icon", store=True
    )
    mobile_show_icon = fields.Boolean(
        "Mobile Icon", compute="_compute_mobile_show_icon", store=True
    )
    addr1_show_icon = fields.Boolean(
        "Address1 Icon", compute="_compute_addr1_show_icon", store=True
    )
    addr2_show_icon = fields.Boolean(
        "Address2 Icon", compute="_compute_addr2_show_icon", store=True
    )
    zip_show_icon = fields.Boolean(
        "Zip Icon", compute="_compute_zip_show_icon", store=True
    )
    city_show_icon = fields.Boolean(
        "City Icon", compute="_compute_city_show_icon", store=True
    )
    state_show_icon = fields.Boolean(
        "State Icon", compute="_compute_state_show_icon", store=True
    )
    country_show_icon = fields.Boolean(
        "Country Icon", compute="_compute_country_show_icon", store=True
    )
    vat_show_icon = fields.Boolean(
        "Vat Icon", compute="_compute_vat_show_icon", store=True
    )
    is_company_show_icon = fields.Boolean(
        "Is Company Icon", compute="_compute_is_company_show_icon", store=True
    )

    @api.depends("name", "name2")
    def _compute_name_show_icon(self):
        for record in self:
            if (not record.name and not record.name2) or (record.name == record.name2):
                record.name_show_icon = True
            else:
                record.name_show_icon = False

    @api.depends("company_id", "company_id")
    def _compute_company_show_icon(self):
        for record in self:
            if (not record.company_id and not record.company_id2) or (
                record.company_id == record.company_id2
            ):
                record.company_show_icon = True
            else:
                record.company_show_icon = False

    @api.depends("company_name", "company_name2")
    def _compute_company_name_show_icon(self):
        for record in self:
            if (not record.company_name and not record.company_name2) or (
                record.company_name == record.company_name2
            ):
                record.company_name_show_icon = True
            else:
                record.company_name_show_icon = False

    @api.depends("email", "email2")
    def _compute_email_show_icon(self):
        for record in self:
            if (not record.email and not record.email2) or (
                record.email2
                and record.email
                and record.email.lower() == record.email2.lower()
            ):
                record.email_show_icon = True
            else:
                record.email_show_icon = False

    @api.depends("phone", "phone2")
    def _compute_phone_show_icon(self):
        for record in self:
            if (not record.phone and not record.phone2) or (
                record.phone == record.phone2
            ):
                record.phone_show_icon = True
            else:
                record.phone_show_icon = False

    @api.depends("mobile", "mobile2")
    def _compute_mobile_show_icon(self):
        for record in self:
            if (not record.mobile and not record.mobile2) or (
                record.mobile == record.mobile2
            ):
                record.mobile_show_icon = True
            else:
                record.mobile_show_icon = False

    @api.depends("street", "street2")
    def _compute_addr1_show_icon(self):
        for record in self:
            if (not record.street and not record.street2) or (
                record.street == record.street2
            ):
                record.addr1_show_icon = True
            else:
                record.addr1_show_icon = False

    @api.depends("street11", "street22")
    def _compute_addr2_show_icon(self):
        for record in self:
            if (not record.street11 and not record.street22) or (
                record.street11 == record.street22
            ):
                record.addr2_show_icon = True
            else:
                record.addr2_show_icon = False

    @api.depends("zip", "zip2")
    def _compute_zip_show_icon(self):
        for record in self:
            if (not record.zip and not record.zip2) or (record.zip == record.zip2):
                record.zip_show_icon = True
            else:
                record.zip_show_icon = False

    @api.depends("city", "city2")
    def _compute_city_show_icon(self):
        for record in self:
            if (not record.city and not record.city2) or (record.city == record.city2):
                record.city_show_icon = True
            else:
                record.city_show_icon = False

    @api.depends("state_id", "state_id2")
    def _compute_state_show_icon(self):
        for record in self:
            if (not record.state_id and not record.state_id2) or (
                record.state_id == record.state_id2
            ):
                record.state_show_icon = True
            else:
                record.state_show_icon = False

    @api.depends("country_id", "country_id2")
    def _compute_country_show_icon(self):
        for record in self:
            if (not record.country_id and not record.country_id2) or (
                record.country_id == record.country_id2
            ):
                record.country_show_icon = True
            else:
                record.country_show_icon = False

    @api.depends("vat_1", "vat_2")
    def _compute_vat_show_icon(self):
        for record in self:
            if (not record.vat_1 and not record.vat_2) or (
                record.vat_1 == record.vat_2
            ):
                record.vat_show_icon = True
            else:
                record.vat_show_icon = False

    @api.depends("is_company", "is_company2")
    def _compute_is_company_show_icon(self):
        for record in self:
            if (not record.is_company and not record.is_company2) or (
                record.is_company == record.is_company2
            ):
                record.is_company_show_icon = True
            else:
                record.is_company_show_icon = False

    @api.onchange("keep1")
    def _onchange_keep1(self):
        if self.keep1:
            self.keep2 = False
            self.dst_partner_id = self.partner_ids and self.partner_ids[0].id or False

    @api.onchange("keep2")
    def _onchange_keep2(self):
        if self.keep2:
            self.keep1 = False
            self.dst_partner_id = self.partner_ids and self.partner_ids[1].id or False

    def action_skip(self):
        if self.partner_wizard_id.current_line_id:
            skipped_partner_ids = self.partner_ids.ids
            new_aggr_ids = list(
                set(literal_eval(self.partner_wizard_id.current_line_id.aggr_ids))
                - set(skipped_partner_ids)
            )
            if not new_aggr_ids or len(new_aggr_ids) == 1:
                self.partner_wizard_id.current_line_id.unlink()
            else:
                self.partner_wizard_id.current_line_id.write({"aggr_ids": new_aggr_ids})
        else:
            return {
                "warning": {"title": _("Warning"), "message": _("No duplicates found")}
            }

        self.partner_wizard_id.write(
            {
                "duplicate_position": self.partner_wizard_id.duplicate_position + 1,
            }
        )
        return self.partner_wizard_id._action_new_next_screen()

    def _get_ordered_partner(self, partner_ids, context=None):
        partners = self.pool.get("res.partner").browse(
            list(partner_ids), context=context
        )
        ordered_partners = sorted(
            sorted(partners, key=operator.attrgetter("create_date"), reverse=True),
            key=operator.attrgetter("active"),
            reverse=True,
        )
        return ordered_partners

    def _merge(self, partner_ids, dst_partner=None, context=None):
        # super-admin can be used to bypass extra checks
        if self.env.user._is_admin():
            pass

        Partner = self.env["res.partner"]
        partner_ids = Partner.browse(partner_ids).exists()
        if len(partner_ids) < 2:
            return
        if len(partner_ids) > 3:
            raise UserError(
                _(
                    "For safety reasons, you cannot merge more"
                    " than 3 contacts together. You can re-open the wizard "
                    "several times if needed."
                )
            )

        # check if the list of partners to merge contains child/parent relation
        child_ids = self.env["res.partner"]
        for partner_id in partner_ids:
            child_ids |= (
                Partner.search([("id", "child_of", [partner_id.id])]) - partner_id
            )
        if partner_ids & child_ids:
            raise UserError(_("You cannot merge a contact with one of his parent."))

        if len({partner.email.lower() for partner in partner_ids}) > 1:
            raise UserError(
                _(
                    "All contacts must have the same email. Only the "
                    "Administrator can merge contacts with different emails."
                )
            )

        # remove dst_partner from partners to merge
        if dst_partner and dst_partner in partner_ids:
            src_partners = partner_ids - dst_partner
        else:
            ordered_partners = self._get_ordered_partner(partner_ids.ids)
            dst_partner = ordered_partners[-1]
            src_partners = ordered_partners[:-1]
        _logger.info("dst_partner: %s", dst_partner.id)

        # Make the company of all related users consistent
        if dst_partner.company_id:
            for user in partner_ids.mapped("user_ids"):
                user.sudo().write(
                    {
                        "company_ids": [(6, 0, [dst_partner.company_id.id])],
                        "company_id": dst_partner.company_id.id,
                    }
                )

        # call sub methods to do the merge
        self._update_foreign_keys(src_partners, dst_partner)
        self._update_reference_fields(src_partners, dst_partner)
        self._update_values(src_partners, dst_partner)

        self._log_merge_operation(src_partners, dst_partner)

        for partner in src_partners:
            partner.unlink()

    # delete source partner, since they are merged
    def _log_merge_operation(self, src_partners, dst_partner):
        _logger.info(
            "(uid = %s) merged the partners %r with %s",
            self._uid,
            src_partners.ids,
            dst_partner.id,
        )

    def _update_foreign_keys(self, src_partners, dst_partner, context=None):
        res = self.env["base.partner.merge.automatic.wizard"]._update_foreign_keys(
            src_partners, dst_partner
        )
        return res

    def _update_reference_fields(self, src_partners, dst_partner, context=None):
        res = self.env["base.partner.merge.automatic.wizard"]._update_reference_fields(
            src_partners, dst_partner
        )
        return res

    @api.model
    def _update_values(self, src_partners, dst_partner):
        _logger.debug(
            "_update_values for dst_partner: %s for src_partners: %r",
            dst_partner.id,
            src_partners.ids,
        )

        model_fields = dst_partner.fields_get().keys()

        def write_serializer(item):
            if isinstance(item, models.BaseModel):
                return item.id
            else:
                return item

        # get all fields that are not computed or x2many
        values = dict()

        form_fields = [
            "name",
            "email",
            "phone",
            "street",
            "street2",
            "zip",
            "city",
            "state_id",
            "country_id",
            "is_company",
            "vat",
        ]
        for column in model_fields:
            field = dst_partner._fields[column]
            if (
                field.type not in ("many2many", "one2many")
                and field.compute is None
                and column not in form_fields
            ):
                for item in itertools.chain(src_partners, [dst_partner]):
                    if item[column]:
                        values[column] = write_serializer(item[column])

        # remove fields that can not be updated (id and parent_id)
        values.pop("id", None)
        parent_id = values.pop("parent_id", None)
        if dst_partner.child_ids and "is_company" not in values:
            values.update({"is_company": dst_partner.is_company})
        dst_partner.write(values)
        # try to update the parent_id
        if parent_id and parent_id != dst_partner.id:
            try:
                dst_partner.write({"parent_id": parent_id})
            except ValidationError:
                _logger.info(
                    "Skip recursive partner hierarchies for parent_id %s of partner: %s",
                    parent_id,
                    dst_partner.id,
                )

    def action_merge(self, context=None):
        context = dict(context or {}, active_test=False)
        this = self
        if this.keep1 is False and this.keep2 is False:
            raise Warning(_("Please select a contact to keep."))
        if this.keep1:
            this.dst_partner_id = this.partner_ids and this.partner_ids[0].id or False
            if this.dst_partner_id:
                this.dst_partner_id.write(
                    {
                        "parent_id": this.company_id and this.company_id.id or False,
                        "company_name": this.company_name or False,
                        "name": this.name or False,
                        "email": this.email or False,
                        "phone": this.phone or False,
                        "mobile": this.mobile or False,
                        "street": this.street or False,
                        "street2": this.street11 or False,
                        "zip": this.zip or False,
                        "city": this.city or False,
                        "state_id": this.state_id and this.state_id.id or False,
                        "country_id": this.country_id and this.country_id.id or False,
                        "is_company": this.is_company2 or False,
                        "vat": this.vat_1 or False,
                    }
                )
                # To Avoid VAT Validation, updated it using query.
                if this.vat_1:
                    self._cr.execute(
                        """
                        "UPDATE res_partner SET vat IN %s WHERE id IN %s"
                    """,
                        (tuple(this.vat_1), tuple(this.dst_partner_id.id)),
                    )
        else:
            this.dst_partner_id = this.partner_ids and this.partner_ids[1].id or False
            if this.dst_partner_id:
                this.dst_partner_id.write(
                    {
                        "parent_id": this.company_id2 and this.company_id2.id or False,
                        "company_name": this.company_name2 or False,
                        "name": this.name2 or False,
                        "email": this.email2 or False,
                        "phone": this.phone2 or False,
                        "mobile": this.mobile2 or False,
                        "street": this.street2 or False,
                        "street2": this.street22 or False,
                        "zip": this.zip2 or False,
                        "city": this.city2 or False,
                        "state_id": this.state_id2 and this.state_id2.id or False,
                        "country_id": this.country_id2 and this.country_id2.id or False,
                        "is_company": this.is_company2 or False,
                        "vat": this.vat_2 or False,
                    }
                )

                # To Avoid VAT Validation, updated it using query.
                if this.vat_2:
                    self._cr.execute(
                        """
                        UPDATE res_partner SET vat IN %s WHERE id IN %s
                        """,
                        (tuple(this.vat_2), tuple(this.dst_partner_id.id)),
                    )

        partner_ids = set(map(int, this.partner_ids))  # [:2]
        #         custom_partner_ids = set(map(int, this.custom_partner_ids))
        if not partner_ids:
            this.write({"state": "finished"})
            return {
                "type": "ir.actions.act_window",
                "res_model": this._name,
                "res_id": this.id,
                "view_mode": "form",
                "target": "new",
            }

        self._merge(partner_ids, this.dst_partner_id, context=context)

        if this.partner_wizard_id.current_line_id:
            deleted_partner_ids = list(set(partner_ids) - {this.dst_partner_id.id})
            new_aggr_ids = list(
                set(literal_eval(this.partner_wizard_id.current_line_id.aggr_ids))
                - set(deleted_partner_ids)
            )
            if not new_aggr_ids or len(new_aggr_ids) == 1:
                this.partner_wizard_id.current_line_id.unlink()
            else:
                this.partner_wizard_id.current_line_id.write({"aggr_ids": new_aggr_ids})

        this.partner_wizard_id.write(
            {
                "duplicate_position": this.partner_wizard_id.duplicate_position + 1,
            }
        )

        return this.partner_wizard_id._action_new_next_screen()

    def swap_to_left(self):
        context = self._context.get("field_name")
        if context == "company_id2":
            self.company_id = self.company_id2
        if context == "company_name2":
            self.company_name = self.company_name2
        if context == "name2":
            self.name = self.name2
        if context == "email2":
            self.email = self.email2
        if context == "phone2":
            self.phone = self.phone2
        if context == "mobile2":
            self.mobile = self.mobile2
        if context == "street2":
            self.street = self.street2
        if context == "street22":
            self.street11 = self.street22
        if context == "zip2":
            self.zip = self.zip2
        if context == "city2":
            self.city = self.city2
        if context == "state_id2":
            self.state_id = self.state_id2
        if context == "country_id2":
            self.country_id = self.country_id2
        if context == "is_company2":
            self.is_company = self.is_company2
        if context == "vat_2":
            self.vat_1 = self.vat_2

        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }

    def swap_to_right(self):
        context = self._context.get("field_name")
        if context == "company_id":
            self.company_id2 = self.company_id
        if context == "company_name":
            self.company_name2 = self.company_name
        if context == "name":
            self.name2 = self.name
        if context == "email":
            self.email2 = self.email
        if context == "phone":
            self.phone2 = self.phone
        if context == "mobile":
            self.mobile2 = self.mobile
        if context == "street":
            self.street2 = self.street
        if context == "street11":
            self.street22 = self.street11
        if context == "zip":
            self.zip2 = self.zip
        if context == "city":
            self.city2 = self.city
        if context == "state_id":
            self.state_id2 = self.state_id.id
        if context == "country_id":
            self.country_id2 = self.country_id.id
        if context == "is_company":
            self.is_company2 = self.is_company
        if context == "vat_1":
            self.vat_2 = self.vat_1

        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }

    def dummy_button(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }
