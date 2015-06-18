# -*- coding: utf-8 -*-
##############################################################################
#
#    Partner Address on Map module for OpenERP
#    Copyright (C) 2015 Akretion (http://www.akretion.com/)
#    @author: Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import Warning


class MapUrl(models.Model):
    _name = 'map.url'
    _description = 'Map System'

    name = fields.Char(string='Map Provider', required=True)
    address_url = fields.Char(
        string='URL that uses the address',
        help="Odoo will add the address as string at the end of this URL.")
    lat_lon_url = fields.Char(
        string='URL that uses latitude and longitude',
        help="In this URL, {LATITUDE} will be replaced by the latitude and "
        "{LONGITUDE} will be replaced by the longitude (requires the module "
        "base_geolocalize)")


class ResUsers(models.Model):
    _inherit = 'res.users'

    # begin with context_ to allow user to change it by himself
    context_map_url_id = fields.Many2one(
        'map.url', string='Map Provider')

    # called from post-install script
    # I can't use a default method on the field, because it would be executed
    # before loading map_url_data.xml, so it would not be able to set a value
    @api.model
    def _default_map_url(self):
        users = self.env['res.users'].search([])
        map_url = self.env['map.url'].search([], limit=1)
        users.write({'context_map_url_id': map_url.id})


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def open_map(self):
        if not self.env.user.context_map_url_id:
            raise Warning(
                _('Missing map provider: '
                  'you should set it in your preferences.'))
        map_url = self.env.user.context_map_url_id
        if (
                map_url.lat_lon_url and
                hasattr(self, 'partner_latitude') and
                self.partner_latitude and self.partner_longitude):
            url = map_url.lat_lon_url.replace(
                '{LATITUDE}', unicode(self.partner_latitude))
            url = url.replace('{LONGITUDE}', unicode(self.partner_longitude))
        else:
            if not map_url.address_url:
                raise Warning(
                    _("Missing parameter 'URL that uses the address' "
                      "for map provider '%s'.") % map_url.name)
            url = map_url.address_url
            if self.street:
                url += self.street
            if self.street2:
                url += ' ' + self.street2
            if self.city:
                url += ' ' + self.city
            if self.state_id:
                url += ' ' + self.state_id.name
            if self.country_id:
                url += ' ' + self.country_id.name
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
            }
