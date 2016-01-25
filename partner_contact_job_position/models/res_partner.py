# -*- coding: utf-8 -*-
#    Copyright (c) 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
#    Copyright (c) 2015 Antiun Ingeniería S.L. (http://www.antiun.com)
#                       Antonio Espinosa <antonioea@antiun.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    job_position_id = fields.Many2one(
        "res.partner.job_position",
        "Categorized job position",
        oldname="job_position")


class ResPartnerJobPosition(models.Model):
    _name = "res.partner.job_position"
    _order = "parent_left"
    _parent_order = "name"
    _parent_store = True
    _description = "Job position"

    name = fields.Char(required=True, translate=True)
    parent_id = fields.Many2one(
        "res.partner.job_position",
        "Parent", ondelete='restrict')
    child_ids = fields.One2many(
        "res.partner.job_position",
        "parent_id",
        "Children",
        oldname="children")
    parent_left = fields.Integer(index=True)
    parent_right = fields.Integer(index=True)
