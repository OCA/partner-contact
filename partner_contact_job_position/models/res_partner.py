# Copyright 2014 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2015 Antonio Espinosa <antonioea@antiun.com>
# Copyright 2015 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    job_position_id = fields.Many2one(
        "res.partner.job_position", "Categorized job position"
    )


class ResPartnerJobPosition(models.Model):
    _name = "res.partner.job_position"
    _description = "Job position"

    name = fields.Char(required=True, translate=True)
