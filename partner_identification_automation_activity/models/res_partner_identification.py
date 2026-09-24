from dateutil.relativedelta import relativedelta

from odoo import api, models


class ResPartnerIdNumber(models.Model):
    _inherit = "res.partner.id_number"

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to also create initial check activities when needed"""
        records = super().create(vals_list)

        # Prepare activity values for batch creation
        # for records that need initial activities
        activity_values_list = []
        model_id = self.env["ir.model"]._get("res.partner.id_number").id

        for record in records:
            # Check if the category is configured to create initial activities
            # Reload the category to make sure it's properly loaded
            category = record.category_id
            if (
                category
                and category.create_activity_on_new
                and record.status == "draft"
            ):
                # Use category-specific initial activity type if configured,
                # otherwise use the default
                activity_type = category.initial_activity_type_id

                if not activity_type:
                    # Fall back to the module-defined activity type for initial checks
                    activity_type = self.env.ref(
                        "partner_identification_automation_activity.mail_activity_type_initial_check_id",
                        raise_if_not_found=False,
                    )

                if not activity_type:
                    # Fall back to generic "To Do" if specific type not available
                    activity_type = self.env.ref(
                        "mail.mail_activity_data_todo", raise_if_not_found=False
                    )
                    if not activity_type:
                        activity_type = self.env["mail.activity.type"].search(
                            [("name", "=", "To Do")], limit=1
                        )

                # Ensure we have a valid activity type before continuing
                if activity_type and activity_type.exists():
                    # Assign to category responsible user, or fall back to current user
                    assigned_user = category.responsible_user_id or self.env.user
                    # Use the activity type's summary and include the ID number
                    summary = (
                        activity_type.summary or "Initial check identification document"
                    )
                    if record.name not in summary:
                        summary = f"{summary}: {record.name}"
                    activity_values = {
                        "activity_type_id": activity_type.id,
                        "summary": summary,
                        "note": activity_type.default_note
                        or (
                            f'Perform initial check for ID "{record.name}" '
                            f'for partner "{record.partner_id.name}".'
                        ),
                        "res_id": record.id,
                        "res_model_id": model_id,
                        "user_id": assigned_user.id,
                    }
                    activity_values_list.append(activity_values)

        # Batch create all required activities in a single operation
        if activity_values_list:
            self.env["mail.activity"].sudo().create(activity_values_list)

        return records

    def _create_renewal_activities(self):
        """Create mail activities for IDs that need renewal"""
        # Find records that don't have an open activity for renewal yet
        model_id = self.env["ir.model"]._get(self._name).id
        activities_vals = []

        for record in self:
            # Only process records that have valid validity dates
            if not record.valid_until:
                continue  # Skip records without expiry date since we can't
                # calculate deadline

            # Reload the category to ensure it's properly loaded
            category = record.category_id
            # Get the appropriate activity type for this record based on its category
            record_activity_type = (
                category.renew_activity_type_id
                if (
                    category
                    and category.renew_activity_type_id
                    and category.renew_activity_type_id.exists()
                )
                else None
            )

            # If no custom activity type in category, use the default one from module
            if not record_activity_type:
                record_activity_type = self.env.ref(
                    "partner_identification_automation_activity.mail_activity_type_renew_id",
                    raise_if_not_found=False,
                )

            # If still no activity type, use fallback
            if not record_activity_type:
                record_activity_type = self.env.ref(
                    "mail.mail_activity_data_todo", raise_if_not_found=False
                )
                if not record_activity_type:
                    record_activity_type = self.env["mail.activity.type"].search(
                        [("name", "=", "To Do")], limit=1
                    )

            # Verify the activity type exists before proceeding
            if not record_activity_type or not record_activity_type.exists():
                continue  # Skip if we can't determine the appropriate activity type

            # Check if an activity of this type already exists for this record
            existing_activity = (
                self.env["mail.activity"]
                .sudo()
                .search(
                    [
                        ("res_model_id", "=", model_id),
                        ("res_id", "=", record.id),
                        ("activity_type_id", "=", record_activity_type.id),
                        ("date_done", "=", False),
                    ],
                    limit=1,
                )
            )

            if existing_activity:
                continue  # Skip if activity already exists

            assigned_user = category.responsible_user_id or self.env.user
            deadline = record.valid_until
            if category.renewal_lead_unit and category.renewal_lead_number:
                deadline -= relativedelta(
                    **{category.renewal_lead_unit: category.renewal_lead_number}
                )

            # Use the activity type's summary and include the ID number
            summary = record_activity_type.summary or "Renew identification document"
            if record.name not in summary:
                summary = f"{summary}: {record.name}"

            activities_vals.append(
                {
                    "activity_type_id": record_activity_type.id,
                    "summary": summary,
                    "note": record_activity_type.default_note
                    or f'ID "{record.name}" for "{record.partner_id.name}".',
                    "res_id": record.id,
                    "res_model_id": model_id,
                    "user_id": assigned_user.id,
                    "date_deadline": deadline,
                }
            )

        if activities_vals:
            self.env["mail.activity"].sudo().create(activities_vals)

    def write(self, vals):
        """Override write to create activities when status changes to 'pending'"""
        # Store original records and old values before changes
        old_values = {}

        if "status" in vals and vals["status"] == "pending":
            # Capture old status values before the write operation
            old_values = {record.id: record.status for record in self}

        # Execute the write operation
        result = super().write(vals)

        # Process renewal activities for records that changed from non-pending to
        # pending
        if "status" in vals and vals["status"] == "pending":
            records_that_changed = self.filtered(
                lambda r: old_values.get(r.id)
                and old_values.get(r.id) != "pending"
                and r.status == "pending"
            )
            if records_that_changed:
                records_that_changed._create_renewal_activities()

        return result
