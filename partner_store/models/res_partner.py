# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, _
from odoo.tools.misc import format_date
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    type = fields.Selection(selection_add=[('store', 'Store Address')])

    def _avatar_get_placeholder_path(self):
        if self.type == 'store':
            return "partner_store/static/img/store.png"
        return super()._avatar_get_placeholder_path()    