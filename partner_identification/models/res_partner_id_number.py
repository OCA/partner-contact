# -*- coding: utf-8 -*-
#
# © 2004-2010 Tiny SPRL http://tiny.be
# © 2010-2012 ChriCar Beteiligungs- und Beratungs- GmbH
#             http://www.camptocamp.at
# © 2015 Antiun Ingenieria, SL (Madrid, Spain)
#        http://www.antiun.com
#        Antonio Espinosa <antonioea@antiun.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, models, fields


class ResPartnerIdNumber(models.Model):
    _name = "res.partner.id_number"
    _order = "name"

    @api.constrains('name')
    def validate_id_number(self):
        self.category_id.validate_id_number(self)

    name = fields.Char(string="ID Number", required=True)
    category_id = fields.Many2one(string="Category", required=True,
                                  comodel_name='res.partner.id_category')
    partner_id = fields.Many2one(string="Partner", required=True,
                                 comodel_name='res.partner')
    partner_issued_id = fields.Many2one(string="Issued by",
                                        comodel_name='res.partner')
    date_issued = fields.Date(string="Issued on")
    valid_from = fields.Date(string="Valid from")
    valid_until = fields.Date(string="Valid until")
    comment = fields.Text(string="Notes")
    state = fields.Char(string="State", size=16)
    active = fields.Boolean(string="Active", default=True)
