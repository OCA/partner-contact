# -*- coding: utf-8 -*-
# Copyright 2016 Ursa Information Systems <http://ursainfosystems.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    caloric_intake = fields.Float("Calories")
    caloric_intake_uom = fields.Many2one("product.uom", "Calories UoM")
    carbohydrate_intake = fields.Float("Carbohydrate")
    carbohydrate_intake_uom = fields.Many2one("product.uom",
                                              "Carbohydrate UoM")
    fat_intake = fields.Float("Fat")
    fat_intake_uom = fields.Many2one("product.uom", "Fat UoM")
    protein_intake = fields.Float("Protein")
    protein_intake_uom = fields.Many2one("product.uom", "Protein UoM")
