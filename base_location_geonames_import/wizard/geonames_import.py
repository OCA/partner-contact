# -*- coding: utf-8 -*-
##############################################################################
#
#    Base Location Geonames Import module for OpenERP
#    Copyright (C) 2014 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#    Copyright (C) 2014 Agile Business Group (http://www.agilebg.com)
#    @author Lorenzo Battistini <lorenzo.battistini@agilebg.com>
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
import requests
import tempfile
import StringIO
import zipfile
import os
import logging

try:
    import unicodecsv
except ImportError:
    unicodecsv = None

logger = logging.getLogger(__name__)


class BetterZipGeonamesImport(models.TransientModel):
    _name = 'better.zip.geonames.import'
    _description = 'Import Better Zip from Geonames'
    _rec_name = 'country_id'

    country_id = fields.Many2one('res.country', 'Country', required=True)
    title_case = fields.Boolean(
        string='Title Case',
        help='Converts retreived city and state names to Title Case.',
    )

    @api.model
    def transform_city_name(self, city, country):
        """Override it for transforming city name (if needed)
        :param city: Original city name
        :param country: Country record
        :return: Transformed city name
        """
        return city

    @api.model
    def _domain_search_better_zip(self, row, country):
        return [('name', '=', row[1]),
                ('city', '=', self.transform_city_name(row[2], country)),
                ('country_id', '=', country.id)]

    @api.model
    def _prepare_better_zip(self, row, country):
        state = self.select_or_create_state(row, country)
        vals = {
            'name': row[1],
            'city': self.transform_city_name(row[2], country),
            'state_id': state.id,
            'country_id': country.id,
            }
        return vals

    @api.model
    def create_better_zip(self, row, country):
        if row[0] != country.code:
            raise Warning(
                _("The country code inside the file (%s) doesn't "
                    "correspond to the selected country (%s).")
                % (row[0], country.code))
        logger.debug('ZIP = %s - City = %s' % (row[1], row[2]))
        if (self.title_case):
            row[2] = row[2].title()
            row[3] = row[3].title()
        if row[1] and row[2]:
            zip_model = self.env['res.better.zip']
            zips = zip_model.search(self._domain_search_better_zip(
                row, country))
            if zips:
                return zips[0]
            else:
                vals = self._prepare_better_zip(row, country)
                if vals:
                    return zip_model.create(vals)
        else:
            return False

    @api.model
    def select_or_create_state(
            self, row, country, code_row_index=4, name_row_index=3):
        states = self.env['res.country.state'].search([
            ('country_id', '=', country.id),
            ('code', '=', row[code_row_index]),
            ])
        if len(states) > 1:
            raise Warning(
                _("Too many states with code %s for country %s")
                % (row[code_row_index], country.code))
        if len(states) == 1:
            return states[0]
        else:
            return self.env['res.country.state'].create({
                'name': row[name_row_index],
                'code': row[code_row_index],
                'country_id': country.id
                })

    @api.one
    def run_import(self):
        zip_model = self.env['res.better.zip']
        country_code = self.country_id.code
        config_url = self.env['ir.config_parameter'].get_param(
            'geonames.url',
            default='http://download.geonames.org/export/zip/%s.zip')
        url = config_url % country_code
        logger.info('Starting to download %s' % url)
        res_request = requests.get(url)
        if res_request.status_code != requests.codes.ok:
            raise Warning(
                _('Got an error %d when trying to download the file %s.')
                % (res_request.status_code, url))
        # Store current record list
        zips_to_delete = zip_model.search(
            [('country_id', '=', self.country_id.id)])
        f_geonames = zipfile.ZipFile(StringIO.StringIO(res_request.content))
        tempdir = tempfile.mkdtemp(prefix='openerp')
        f_geonames.extract('%s.txt' % country_code, tempdir)
        logger.info('The geonames zipfile has been decompressed')
        data_file = open(os.path.join(tempdir, '%s.txt' % country_code), 'r')
        data_file.seek(0)
        logger.info('Starting to create the better zip entries')
        for row in unicodecsv.reader(
                data_file, encoding='utf-8', delimiter='	'):
            zip = self.create_better_zip(row, self.country_id)
            if zip in zips_to_delete:
                zips_to_delete -= zip
        data_file.close()
        if zips_to_delete:
            zips_to_delete.unlink()
            logger.info('%d better zip entries deleted for country %s' %
                        (len(zips_to_delete), self.country_id.name))
        logger.info(
            'The wizard to create better zip entries from geonames '
            'has been successfully completed.')
        return True
