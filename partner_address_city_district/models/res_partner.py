# Copyright 2022 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import etree
from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    city_district_id = fields.Many2one(
        'res.city.district', domain="[('city_id', '=', city_id)]",
    )

    @api.model
    def _fields_view_get_address(self, arch):
        arch = super()._fields_view_get_address(arch)
        # render the partner address accordingly to address_view_id
        document = etree.fromstring(arch)
        if document.xpath("//field[@name='city_district_id']"):  # pragma: no cover
            return arch
        for node in document.xpath("//field[@name='city_id']"):
            node.addnext(etree.Element("field", attrib={
                "name": "city_district_id",
                "attrs": """{
                    'invisible': [('country_enforce_cities', '=', False)],
                }""",
                "placeholder": _("District"),
                "class": "o_address_city",
                "context": """{
                    'default_city_id': 'city_id',
                }""",
            }))
        return etree.tostring(document)
