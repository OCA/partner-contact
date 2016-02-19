# -*- coding: utf-8 -*-
# © 2016 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from openerp import api, models

_logger = logging.getLogger(__name__)


class IrModel(models.Model):
    _inherit = "ir.model"

    @api.cr
    def _register_hook(self, cr):
        """Only warn in installed instances."""
        _logger.info("WARNING: This module is DEPRECATED. See README.")
        return super(IrModel, self)._register_hook(cr)
