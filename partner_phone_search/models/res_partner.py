# Copyright 2018 - TODAY Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            domain = ['|', '|', ('phone', operator, name),
                      ('mobile', operator, name), ('email', operator, name)
                      ]
            partners = self.search(domain + args, limit=limit,)
            res = partners.name_get()
            if limit:
                limit_rest = limit - len(partners)
            else:
                limit_rest = limit
            if limit_rest or not limit:
                args += [('id', 'not in', partners.ids)]
                res += super(ResPartner, self).name_search(
                    name, args=args, operator=operator, limit=limit_rest)
            return res
