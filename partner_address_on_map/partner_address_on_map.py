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
        help="In this URL, {ADDRESS} will be replaced by the address.")
    lat_lon_url = fields.Char(
        string='URL that uses latitude and longitude',
        help="In this URL, {LATITUDE} and {LONGITUDE} will be replaced by "
        "the latitude and longitude (requires the module 'base_geolocalize')")
    route_address_url = fields.Char(
        string='Route URL that uses the addresses',
        help="In this URL, {START_ADDRESS} and {DEST_ADDRESS} will be "
        "replaced by the start and destination addresses.")
    route_lat_lon_url = fields.Char(
        string='Route URL that uses latitude and longitude',
        help="In this URL, {START_LATITUDE}, {START_LONGITUDE}, "
        "{DEST_LATITUDE} and {DEST_LONGITUDE} will be replaced by the "
        "latitude and longitude of the start and destination adresses "
        "(requires the module 'base_geolocalize').")


class ResUsers(models.Model):
    _inherit = 'res.users'

    # begin with context_ to allow user to change it by himself
    context_map_url_id = fields.Many2one('map.url', string='Map Provider')
    # IDEA : should we add the ability to have 1 map provider for map
    # and another one for routing ?
    context_route_start_partner_id = fields.Many2one(
        'res.partner', string='Start Address for Route Map')

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

    @api.model
    def address_as_string(self):
        addr = u''
        if self.street:
            addr += self.street
        if self.street2:
            addr += u' ' + self.street2
        if self.city:
            addr += u' ' + self.city
        if self.state_id:
            addr += u' ' + self.state_id.name
        if self.country_id:
            addr += u' ' + self.country_id.name
        return addr

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
            url = map_url.address_url.replace(
                '{ADDRESS}', self.address_as_string())
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
            }

    @api.multi
    def open_route_map(self):
        if not self.env.user.context_map_url_id:
            raise Warning(
                _('Missing map provider: '
                  'you should set it in your preferences.'))
        map_url = self.env.user.context_map_url_id
        if not self.env.user.context_route_start_partner_id:
            raise Warning(
                _('Missing start address for route map: '
                  'you should set it in your preferences.'))
        start_partner = self.env.user.context_route_start_partner_id
        if map_url.route_address_url:
            start_address = start_partner.address_as_string()
            dest_address = self.address_as_string()
            url = map_url.route_address_url
            url = url.replace('{START_ADDRESS}', start_address)
            url = url.replace('{DEST_ADDRESS}', dest_address)
        else:
            if not hasattr(self, 'partner_latitude'):
                raise Warning(
                    _("Missing module 'base_geolocalize'"))
            if not map_url.route_lat_lon_url:
                raise Warning(
                    _("No route URL that uses latitude and longitude "
                      "on map provider '%s'.") % map_url.name)
            url = map_url.route_lat_lon_url
            if (
                    not start_partner.partner_latitude or
                    not start_partner.partner_longitude):
                raise Warning(
                    _("Missing geo-localization information on "
                      "start partner '%s'."))
            if not self.partner_latitude or not self.partner_longitude:
                raise Warning(
                    _("Missing geo-localization information on destination "
                      "partner '%s'.") % self.name)
            url = url.replace(
                '{START_LATITUDE}', unicode(start_partner.partner_latitude))
            url = url.replace(
                '{START_LONGITUDE}', unicode(start_partner.partner_longitude))
            url = url.replace(
                '{DEST_LATITUDE}', unicode(self.partner_latitude))
            url = url.replace(
                '{DEST_LONGITUDE}', unicode(self.partner_longitude))
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
            }
