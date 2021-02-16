# Copyright 2019 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, _
from odoo.exceptions import ValidationError

class TierValidation(models.AbstractModel):
    _inherit = "tier.validation"

    @api.model
    def _get_under_validation_exceptions(self):
        res = super(TierValidation, self)._get_under_validation_exceptions() or []
        """Extend for more field exceptions."""
        ex_fields = ['categ_id','state', 'customer','supplier','excise_tax']
        for val in ex_fields:
            res.append(val)
        return res

    @api.multi
    def validate_tier(self):
        super(TierValidation, self).validate_tier()
        # make sure to only work with res.partner object.
        if self._name != 'res.partner':
            return        
        for partner in self:
            rec = self.env['tier.review'].search([('res_id','=',partner.id),('model','=','res.partner')])
            if rec and rec.status == 'approved':
                if not (partner.customer or partner.supplier):
                    raise ValidationError(_('Cannot Validate. Please configure partner %s as a Customer or Vendor or Both.') % (partner.display_name))
                else:
                    partner.state = 'approved'

    # Need to override for Partner Tier Validation since can_review field is set to True based only
    # if current user is a member of reviewer_ids. This can_review field is used to enable or disable the boolean
    # field Is Customer / Is Vendor not only during the Validation process but even if it is in Approved State.
    @api.multi
    @api.depends('review_ids')
    def _compute_reviewer_ids(self):
        if str(self.__class__) == "<class 'odoo.api.res.partner'>":            
            for rec in self:
                rec.reviewer_ids = rec.review_ids.filtered(
                    lambda r: r.status in ( 'pending','approved')).mapped('reviewer_ids')
        else:
            for rec in self:
                rec.reviewer_ids = rec.review_ids.filtered(
                    lambda r: r.status == 'pending').mapped('reviewer_ids')

    @api.multi
    def request_validation(self):
        res = super().request_validation()
        for rec in self.filtered(lambda x: x._name == 'res.partner'):
            rec.message_subscribe(partner_ids=[self.env.user.partner_id.id,])
        return res
