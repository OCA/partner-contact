# -*- coding: utf-8 -*-

# Copyright (c) 2004-2015 Odoo S.A. (original module : base_geolocalize)
# © 2018 Le Filament (<http://www.le-filament.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import json
import urllib2

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


def geo_find(addr):
    if not addr:
        return None
    url = 'https://nominatim.openstreetmap.org/search.php/'
    url += urllib2.quote(addr.encode('utf8'))
    url += '?format=json'

    try:
        result = json.load(urllib2.urlopen(url))
    except Exception as e:
        raise UserError(_('Cannot contact geolocation servers. Please make '
                          'sure that your Internet connection is up and '
                          'running (%s).') % e)

    try:
        if result:
            geo = result[0]
            return [float(geo['lat']), float(geo['lon'])]
        else:
            return None
    except (KeyError, ValueError):
        return None


def geo_query_address(street=None, zip=None,
                      city=None, state=None, country=None):
    if (country and ',' in country
            and (country.endswith(' of') or country.endswith(' of the'))):
        country = '{1} {0}'.format(*country.split(',', 1))
    return tools.ustr(', '.join(filter(None, [street, ("%s %s" % (
        zip or '', city or '')).strip(), state, country])))


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_latitude = fields.Float(string='Geo Latitude', digits=(16, 5))
    partner_longitude = fields.Float(string='Geo Longitude', digits=(16, 5))
    date_localization = fields.Date(string='Geolocation Date')

    @api.multi
    def geo_localize(self):
        # We need country names in English below
        for partner in self.with_context(lang='en_US'):
            if partner.city:
                result = geo_find(geo_query_address(
                    street=partner.street,
                    zip=partner.zip, city=partner.city,
                    country=partner.country_id.name
                ))

                if result is None:
                    result = geo_find(geo_query_address(
                        city=partner.city,
                        country=partner.country_id.name
                    ))

                if result:
                    partner.write({
                        'partner_latitude': result[0],
                        'partner_longitude': result[1],
                        'date_localization': fields.Date.context_today(partner)
                    })

        return True
