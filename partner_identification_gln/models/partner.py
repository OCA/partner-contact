# -*- coding: utf-8 -*-
# ©  2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from stdnum import ean
from stdnum.exceptions import InvalidChecksum
from openerp import api, models


class ResPartnerIdCategory(models.Model):
    _inherit = 'res.partner.id_category'

    @api.multi
    def validate_res_partner_gln(self, id_number):
        self.ensure_one()
        if not id_number:
            return False

        try:
            ean.validate(id_number.name)
        except InvalidChecksum:
            return True

        num_obj = self.env['res.partner.id_number']
        duplicate_gln = num_obj.search([('category_id', '=',
                                         id_number.category_id.id),
                                        ('name', '=', id_number.name),
                                        ('name', '!=', False),
                                        ('id', '!=', id_number.id)])

        if duplicate_gln:
            return True

        return False
