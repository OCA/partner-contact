# -*- coding: utf-8 -*-
#
# © 2004-2010 Tiny SPRL http://tiny.be
# © 2010-2012 ChriCar Beteiligungs- und Beratungs- GmbH
#             http://www.camptocamp.at
# © 2015 Antiun Ingenieria, SL (Madrid, Spain)
#        http://www.antiun.com
#        Antonio Espinosa <antonioea@antiun.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import models, fields


class ResPartnerIdCategory(models.Model):
    _name = "res.partner.id_category"
    _order = "name"

    code = fields.Char(string="Code", size=16, required=True)
    name = fields.Char(string="ID name", required=True, translate=True)
    active = fields.Boolean(string="Active", default=True)
