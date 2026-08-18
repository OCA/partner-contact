from odoo import fields, models


class ResPartnerIdCategory(models.Model):
    _inherit = "res.partner.id_category"

    create_activity_on_new = fields.Boolean(
        string="Create Activity on New",
        default=False,
        help="Enable to create an activity when a new identification record is created",
    )

    responsible_user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible User",
        help=(
            "Responsible user for handling activities for "
            "this category of identification records"
        ),
    )

    initial_activity_type_id = fields.Many2one(
        comodel_name="mail.activity.type",
        string="Initial Check Activity Type",
        help="Activity type to use for initial check activities",
    )

    renew_activity_type_id = fields.Many2one(
        comodel_name="mail.activity.type",
        string="Renewal Activity Type",
        help="Activity type to use for renewal activities",
    )
