# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re
from odoo import fields, models, _


class CountryState(models.Model):
    _inherit = 'res.country.state'

    name = fields.Char(translate=True)


class Country(models.Model):
    _inherit = 'res.country'

    title_format = fields.Text(string="Layout in Name views",
                               help="Display format to use for partner belonging to this country.\n\n"
                                    "You can use python-style string pattern with all the fields of the title "
                                    "(for example, use '%(title)s' to display the field 'title') plus"
                                    "\n%(partner)s: use the partner name"
                                    "\n%(academic_title_display)s: the code of the academic_title_display",
                               default='%(title)s %(partner)s %(academic_title_display)s')

    def get_title_fields(self):
        self.ensure_one()
        return re.findall(r'\((.+?)\)', self.title_format)
