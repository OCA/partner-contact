from odoo import api, fields, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    # Computed field to determine if the KYC button should be visible
    show_kyc_button = fields.Boolean(
        string="Show KYC Button",
        compute="_compute_show_kyc_button",
        store=False,
        depends=["id_numbers", "id_numbers.category_id", "id_numbers.status"],
    )

    def _compute_show_kyc_button(self):
        """Compute whether to show the KYC request button."""
        kyc_category = self.env.ref(
            "partner_identification_kyc.kyc_identification_category",
            raise_if_not_found=False,
        )
        if not kyc_category:
            for partner in self:
                partner.show_kyc_button = False
            return

        # Find all partners in self that have an ongoing KYC record
        ongoing_kyc_records = self.env["res.partner.id_number"].search(
            [
                ("partner_id", "in", self.ids),
                ("category_id", "=", kyc_category.id),
                ("status", "in", ["draft", "open", "pending"]),
            ]
        )

        ongoing_kyc_partner_ids = {
            record.partner_id.id for record in ongoing_kyc_records
        }

        for partner in self:
            show_button = True
            if not kyc_category.enable_on_child_contacts and not partner.is_company:
                show_button = False

            if partner.id in ongoing_kyc_partner_ids:
                show_button = False

            partner.show_kyc_button = show_button

    kyc_valid_until = fields.Date(
        string="KYC Valid Until",
        compute="_compute_kyc_valid_until",
        store=True,
    )

    @api.depends(
        "id_numbers.valid_until", "id_numbers.category_id", "id_numbers.status"
    )
    def _compute_kyc_valid_until(self):
        kyc_category = self.env.ref(
            "partner_identification_kyc.kyc_identification_category",
            raise_if_not_found=False,
        )
        for partner in self:
            valid_until_date = False
            if kyc_category:
                kyc_records = partner.id_numbers.filtered(
                    lambda r: r.category_id == kyc_category and r.status == "open"
                )
                # Collect valid_until dates from records that have them
                valid_dates = [
                    rec.valid_until for rec in kyc_records if rec.valid_until
                ]
                if valid_dates:
                    valid_until_date = min(valid_dates)
            partner.kyc_valid_until = valid_until_date

    def action_view_kyc_records(self):
        self.ensure_one()
        kyc_category = self.env.ref(
            "partner_identification_kyc.kyc_identification_category",
            raise_if_not_found=False,
        )
        return {
            "name": "KYC Records",
            "type": "ir.actions.act_window",
            "res_model": "res.partner.id_number",
            "view_mode": "list,form",
            "domain": [
                ("partner_id", "=", self.id),
                ("category_id", "=", kyc_category.id if kyc_category else False),
            ],
        }

    def _create_kyc_record(self):
        """Private helper method to create a new KYC identification record."""
        self.ensure_one()
        kyc_category = self.env.ref(
            "partner_identification_kyc.kyc_identification_category"
        )
        # The identification number (``name``) is auto-assigned from the
        # ``kyc.identification`` sequence by ``res.partner.id_number.create``.
        return self.env["res.partner.id_number"].create(
            {
                "partner_id": self.id,
                "category_id": kyc_category.id,
                "status": "draft",
            }
        )

    def action_request_kyc(self):
        """Create a new KYC identification record in the 'draft' status."""
        self.ensure_one()  # Ensure single record operation
        kyc_category = self.env.ref(
            "partner_identification_kyc.kyc_identification_category"
        )

        # Check if there's already any active ('open', 'pending') or 'draft' status
        # KYC record to prevent duplicates
        existing_kyc = self.id_numbers.filtered(
            lambda r: r.category_id == kyc_category
            and r.status in ["draft", "open", "pending"]
        )

        if existing_kyc:
            raise UserError(
                self.env._("A KYC request has already been submitted for this partner.")
            )

        # Create a new identification number record for the KYC category using helper
        # method
        self._create_kyc_record()

        # Return action to trigger a refresh of the view
        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }

    def ensure_kyc_record(self):
        """
        API function to ensure a KYC record exists for the partner if none currently
        exists.
        If no active KYC identification record exists for a partner (not in 'draft',
        'open', or 'pending' status), this function creates a record in the 'draft'
        status.
        """
        kyc_category = self.env.ref(
            "partner_identification_kyc.kyc_identification_category"
        )

        for partner in self:
            # Check if there's already an active or pending KYC record for this partner
            existing_kyc = partner.id_numbers.filtered(
                lambda r: r.category_id == kyc_category
                and r.status in ["draft", "open", "pending"]
            )

            if not existing_kyc:
                # Create a new identification number record for the KYC category using
                # helper method
                partner.sudo()._create_kyc_record()
