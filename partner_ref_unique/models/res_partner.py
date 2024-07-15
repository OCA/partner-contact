# Copyright 2016 Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.multi
    @api.constrains('ref', 'is_company', 'company_id')
    def _check_ref(self):
        for partner in self:
            mode = partner.company_id.partner_ref_unique
            if (partner.ref and (
                    mode == 'all' or
                    (mode == 'companies' and partner.is_company))):
                domain = [
                    ('id', '!=', partner.id),
                    ('ref', '=', partner.ref),
                ]
                if mode == 'companies':
                    domain.append(('is_company', '=', True))
                other = self.search(domain)

                # active_test is False when called from
                # base.partner.merge.automatic.wizard
                if other and self.env.context.get("active_test", True):
                    raise ValidationError(
                        _("This reference is equal to partner '%s'") %
                        other[0].display_name)
