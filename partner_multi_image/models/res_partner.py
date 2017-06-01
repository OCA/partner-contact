# -*- coding: utf-8 -*-
# Copyright 2009 Sharoon Thomas Open Labs Business Solutions
# Copyright 2014 Tecnativa - Pedro M. Baeza
# Copyright 2015 Antiun Ingeniería S.L. - Jairo Llopis
# Copyright 2016 Sodexis
# Copyright 2017 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

"""Reference core image fields to multi-image variants."""


from openerp import fields, models


class ResPartner(models.Model):

    _name = "res.partner"
    _inherit = [_name, "base_multi_image.owner"]

    image = fields.Binary(
        related='image_main',
        store=False,
    )
    image_medium = fields.Binary(
        related='image_main_medium',
        store=False,
    )
    image_small = fields.Binary(
        related='image_main_small',
        store=False,
    )
