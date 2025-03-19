# Copyright 2025 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    history_change_ids = fields.One2many(
        comodel_name="res.partner.history.change",
        inverse_name="partner_id",
        string="History Changes",
    )
    allow_edit_history_address = fields.Boolean(
        compute="_compute_allow_edit_history_address",
    )

    @api.depends("history_change_ids")
    def _compute_allow_edit_history_address(self):
        for partner in self:
            partner.allow_edit_history_address = partner.env.user.has_group(
                "partner_address_history.group_edit_history_address"
            )

    def tracking_history_fields(self):
        return self._formatting_address_fields() + ["name"]

    def _prepare_display_address(self, without_company=False):
        """Prepare the display address with history tracking.
        This method extends the standard address display to include historical address data.
        When `keep_partner_history` is enabled and a `date_change` is provided in context,
        it will look up and use the address details from that point in time.
        """
        address_format, args = super()._prepare_display_address(without_company)
        date_change = fields.Date.from_string(self.env.context.get("date_change"))
        if not self.env.company.keep_partner_history or not date_change:
            return address_format, args

        history_change = self.history_change_ids.filtered(
            lambda x: x.date_change > date_change
        )[-1:]
        if history_change:
            for field in self.tracking_history_fields():
                args[field] = history_change[field] or ""
        return address_format, args

    def _prepare_history_change(self):
        return {
            "partner_id": self.id,
            "name": self.name,
            "street": self.street,
            "street2": self.street2,
            "city": self.city,
            "state_id": self.state_id.name,
            "zip": self.zip,
            "country_id": self.country_id.name,
            "date_change": fields.Date.context_today(self),
        }

    def write(self, vals):
        if not self.env.company.keep_partner_history:
            return super().write(vals)

        tracking_fields = self.tracking_history_fields()
        # Prepare history records in batch
        history_vals_list = []
        for partner in self:
            # Keep old value
            dict_history = partner._prepare_history_change()
            has_changes = False
            # Update history record with new value (if any)
            for field in vals.keys():
                if field in tracking_fields:
                    has_changes = True
                    # Check if field is many2one type. If so, get name of the record
                    field_type = partner._fields[field].type
                    if field_type == "many2one":
                        dict_history[field] = (
                            partner[field].name if partner[field] else ""
                        )
                        continue
                    dict_history[field] = partner[field]
            if has_changes:
                history_vals_list.append(dict_history)

        # Create history records in batch if any
        if history_vals_list:
            self.env["res.partner.history.change"].sudo().create(history_vals_list)
        return super().write(vals)

    def _get_name(self):
        res = super()._get_name()
        date_change = fields.Date.from_string(self.env.context.get("date_change"))
        if self.env.company.keep_partner_history and date_change:
            # Check name and result from super is same
            # Some context change is not name like `show_address_only`
            if self.name == res.split("\n")[0]:
                history_change = self.history_change_ids.filtered(
                    lambda x: x.date_change > date_change
                )[-1:]
                if history_change:
                    res = res.replace(res.split("\n")[0], history_change.name)
        return res


class ResPartnerHistoryChange(models.Model):
    _name = "res.partner.history.change"
    _description = "Partner History Change"
    _order = "date_change desc, id desc"

    partner_id = fields.Many2one(
        comodel_name="res.partner",
    )
    # Name Change
    name = fields.Char()
    # Address Change
    street = fields.Char()
    street2 = fields.Char()
    city = fields.Char()
    state_id = fields.Char()
    zip = fields.Char()
    country_id = fields.Char()
    date_change = fields.Date(default=fields.Date.context_today)
