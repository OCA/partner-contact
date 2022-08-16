from odoo import api, fields, models
from odoo.exceptions import ValidationError
import logging
class ResPartner(models.Model):
    """Assigns 'ref' from a sequence on creation and copying"""

    _inherit = "res.partner"

    # _sql_constraints = [
    #     (
    #         "default_partnerref",
    #         "unique(ref)",
    #         "Reference must be unique",
    #     )
    # ]

    @api.constrains('ref')
    def _check_ref(self):
        if self.company_type == 'company':
            if self.ref:
                check_ref = self.search([('id', '!=', self.id),('id','not in',self.child_ids.ids),('ref', '!=', False),('ref', '=', self.ref)],limit=1)
                if check_ref:
                    raise ValidationError("The reference must be unique.") 