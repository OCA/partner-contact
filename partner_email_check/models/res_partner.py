# -*- coding: utf-8 -*-
import re
from odoo import api, models, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.constrains('email')
    def constrains_email(self):
        for rec in self:
            self.email_check(rec.email)

    @api.model
    def email_check(self, email):
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                    email):
            return True
        else:
            raise UserError(_('Email Invalid!'))
