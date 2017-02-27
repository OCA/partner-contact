# -*- coding: utf-8 -*-
# Copyright 2015-2017 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class PartnerAcademicTitle(models.Model):
    _name = 'partner.academic.title'

    name = fields.Char(required=True,
                       translate=True
                       )
    sequence = fields.Integer(required=True,
                              help="""defines the order to display titles"""
                              )
    active = fields.Boolean(default=True)
