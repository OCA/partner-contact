# -*- coding: utf-8 -*-

from openerp import SUPERUSER_ID
from openerp.api import Environment


def post_init_hook(cr, pool):
    env = Environment(cr, SUPERUSER_ID, {})
    env['res.partner'].search(
        [('birthdate', "!=", False)])._birthdate_inverse()
