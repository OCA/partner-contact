from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    can_create_contacts = fields.Boolean(
        default=True,
        groups="base.group_system",
        help="If disabled, this user cannot create new contacts/partners.",
    )
