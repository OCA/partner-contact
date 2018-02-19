# -*- coding: utf-8 -*-
# Copyright 2018 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _get_gravatar_image(self, email):
        return False
