from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _get_partners_with_no_parent(self):
        partners_with_no_parent = self.browse()
        for partner in self:
            parent = partner
            while parent.parent_id:
                parent = parent.parent_id
            partners_with_no_parent |= parent
        return partners_with_no_parent

    def _get_partners_depth_dict(self, partners_with_depth_dict, depth=0):
        for partner in self:
            if partner.child_ids:
                partner.child_ids._get_partners_depth_dict(
                    partners_with_depth_dict, depth=depth + 1
                )
            if depth in partners_with_depth_dict.keys():
                partners_with_depth_dict[depth] |= partner
            else:
                partners_with_depth_dict[depth] = partner

    @api.depends("parent_id")
    def _compute_contact_depth(self):
        partners_with_no_parent = self._get_partners_with_no_parent()
        partners_depth_dict = {}
        partners_with_no_parent._get_partners_depth_dict(partners_depth_dict)
        for depth, partners in partners_depth_dict.items():
            partners.depth = depth

    depth = fields.Integer(compute="_compute_contact_depth", store=True, index=True)

    @api.constrains("depth")
    def check_maximum_contact_depth(self):
        max_depth = int(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("partner_contact_restrict_depth.contacts_max_depth", default=0)
        )
        for partner in self:
            if 0 < max_depth < partner.depth:
                raise ValidationError(
                    _(
                        "You have reached the maximum depth for this contact. "
                        "You cannot create childs or modify values. "
                        "Please resolve this contact, before making any change."
                    )
                )

    def write(self, vals):
        # If we try to modify a contact that its depth it is exceeded,
        # don't let execute the write and the ValidationError will be raised
        self.check_maximum_contact_depth()
        return super().write(vals)

    def partners_with_depth_exceeded(self, new_depth):
        return self.env["res.partner"].search([("depth", ">", new_depth)])
