# -*- coding: utf-8 -*-
# © 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    main_nace_id = fields.Many2one(comodel_name='res.partner.nace',
                                   string="Main activity", ondelete='set null')
    secondary_nace_ids = fields.Many2many(comodel_name='res.partner.nace',
                                          string="Other activities",
                                          ondelete='set null')
