from odoo import _, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    def write(self, vals):
        if (
            "category_id" not in vals
            or "allow_smart_tag_modification" in self.env.context
        ):
            return super().write(vals)

        # For each partner being written to, check the tag changes
        for partner in self:
            old_tags = partner.category_id
            # Simulate the result of the write operation to get the new tags
            # The command list is in vals['category_id']
            super(ResPartner, partner).write({"category_id": vals["category_id"]})
            new_tags = partner.category_id
            # Revert the temporary change
            super(ResPartner, partner).write({"category_id": [(6, 0, old_tags.ids)]})

            changed_tags = (old_tags | new_tags) - (old_tags & new_tags)

            if any(tag.smart for tag in changed_tags):
                raise UserError(
                    _(
                        "Manual modification of smart tags is not allowed. "
                        "These tags are assigned automatically."
                    )
                )

        # If the check passes for all partners, proceed with the actual write
        return super().write(vals)
