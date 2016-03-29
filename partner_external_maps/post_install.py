# -*- coding: utf-8 -*-
# © 2015 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author: Alexis de Lattre <alexis.delattre@akretion.com>

from openerp import SUPERUSER_ID


def set_default_map_settings(cr, pool):
    pool['res.users']._default_map_settings(cr, SUPERUSER_ID)
    return
