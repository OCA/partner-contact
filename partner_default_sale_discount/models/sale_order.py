# -*- coding: utf-8 -*-
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from lxml import etree


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    default_sale_discount = fields.Float(
        related="partner_id.commercial_partner_id.default_sale_discount",
        string="Default sales discount (%)",
    )

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        """Inject the default in the context of the line this way for
        making it inheritable.
        """
        res = super(SaleOrder, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu
        )
        if view_type != 'form':  # pragma: no cover
            return res
        eview = etree.fromstring(res['arch'])
        xml_order_line = eview.xpath("//field[@name='order_line']")
        xml_discount = eview.xpath("//field[@name='default_sale_discount']")
        if xml_order_line and xml_discount:
            # This should be handled in "string" mode, as the context can
            # contain a expression that can only be evaled on execution time
            # on the JS web client
            context = xml_order_line[0].get('context', '{}').replace(
                "{", "{'default_discount': default_sale_discount, ", 1
            )
            xml_order_line[0].set('context', context)
            res['arch'] = etree.tostring(eview)
        return res
