from odoo import api, fields, models


class ResPartnerSocialMedia(models.Model):
    _name = "res.partner.socialmedia"
    _description = "Partner Social Media"
    _order = "name"

    name = fields.Char(
        string="Social Media Account",
        required=True,
        help="The Social Media Account username or contact",
    )
    platform_id = fields.Many2one(
        string="Platform",
        required=True,
        comodel_name="res.partner.socialmedia_platform",
        help="Social Medial platform defined in configuration. For example, Facebook, Twitter etc",
    )
    partner_id = fields.Many2one(
        string="Partner", required=True, comodel_name="res.partner", ondelete="cascade"
    )
    
    active = fields.Boolean(default=True)

    @api.model
    def default_get(self, fields):
        res = super(ResPartnerSocialMedia, self).default_get(fields)
        # It seems to be a bug in native odoo that the field partner_id
        # is not in the fields list by default. A workaround is required
        # to force this.
        if "default_partner_id" in self._context and "partner_id" not in fields:
            fields.append("partner_id")
            res["partner_id"] = self._context.get("default_partner_id")
        return res