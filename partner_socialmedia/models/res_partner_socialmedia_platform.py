from odoo import _, fields, models


class ResPartnerSocialMediaPlatform(models.Model):
    _name = "res.partner.socialmedia_platform"
    _description = "Social Media Platform"
    _order = "name"

    name = fields.Char(
        string="Social Media Platform Name",
        required=True,
        translate=True,
        help="Name of this Social Media Platform",
    )