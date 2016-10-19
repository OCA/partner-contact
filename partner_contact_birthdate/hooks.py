# -*- coding: utf-8 -*-

from odoo import SUPERUSER_ID
from odoo.api import Environment


def post_init_hook(cr, pool):
    env = Environment(cr, SUPERUSER_ID, {})
    env['res.partner'].search(
        [('birthdate', "!=", False)])._birthdate_inverse()
