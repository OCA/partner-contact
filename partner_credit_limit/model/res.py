# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 UAB Versada
#    (<http://www.versada.lt>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api
from openerp.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def credit_limit_reached(self, credit_increase=0.0, raise_error=True):
        """
        Returns True (or exception) if credit limit is reached othervise False
        """
        for each in self:
            # credit_limit is synchronized between company and contacts but
            # credit is not
            credit = each.parent_id and each.parent_id.credit or each.credit
            credit_increased = credit + credit_increase
            if each.credit_limit > 0 and credit_increased > each.credit_limit:
                if raise_error:
                    raise ValidationError(
                        "Credit Limit exceeded for partner %s!\n\n"
                        "Credit Limit: %.2f\nExceeding Credit: %.2f\n" % (
                            self.display_name, each.credit_limit,
                            credit_increased))
                return True
