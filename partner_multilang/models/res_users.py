#  -*- coding: utf-8 -*-
#  Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class Users(models.Model):
    _inherit = 'res.users'

    name = fields.Char(translate=True)
