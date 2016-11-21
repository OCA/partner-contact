# -*- coding: utf-8 -*-
# Copyright 2016 Ursa Information Systems <http://ursainfosystems.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    height = fields.Float("Height")
    height_uom = fields.Many2one("product.uom", "Height UoM",
                                 domain="[('category_id', '=', "
                                        "self.env.ref('product.\
                                        uom_categ_length').id)]")
