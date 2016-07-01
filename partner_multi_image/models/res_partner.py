# -*- coding: utf-8 -*-
# © 2009 Sharoon Thomas Open Labs Business Solutions
# © 2014 Serv. Tecnol. Avanzados Pedro M. Baeza
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# © 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

"""Reference core image fields to multi-image variants."""


from openerp import models, fields


class ResPartner(models.Model):

    _name = "res.partner"
    _inherit = [_name, "base_multi_image.owner"]

    image = fields.Binary(
        related='image_main',
        store=False,
        multi=False
    )
