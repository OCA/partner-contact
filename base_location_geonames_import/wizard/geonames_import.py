# -*- encoding: utf-8 -*-
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
import unicodecsv
import zipfile
import os
import logging

logger = logging.getLogger(__name__)


class better_zip_geonames_import(models.TransientModel):
    _name = 'better.zip.geonames.import'
    _description = 'Import Better Zip from Geonames'
    _rec_name = 'country_id'

    country_id = fields.Many2one('res.country', 'Country', required=True)

    @api.model
    def _prepare_better_zip(self, row, country_id):
        state = self.select_or_create_state(row, country_id)
        vals = {
            'name': row[1],
            'city': row[2],
            'state_id': state.id,
            'country_id': country_id,
            }
        return vals

    @api.model
    def create_better_zip(
            self, row, country_id, country_code):
        bzip_id = False
        if row[0] != country_code:
            raise Warning(
                _('Error:'),
                _("The country code inside the file (%s) doesn't "
                    "correspond to the selected country (%s).")
                % (row[0], country_code))
        logger.debug('ZIP = %s - City = %s' % (row[1], row[2]))
        if row[1] and row[2]:
            vals = self._prepare_better_zip(row, country_id)
            if vals:
                bzip_id = self.env['res.better.zip'].create(vals)
        return bzip_id

    @api.model
    def select_or_create_state(
        self, row, country_id, code_row_index=4, name_row_index=3
    ):
        states = self.env['res.country.state'].search([
            ('country_id', '=', country_id),
            ('code', '=', row[code_row_index]),
            ])
        if len(states) > 1:
            raise Warning(
                _("Too many states with code %s for counrty %s")
                % (row[code_row_index], country_id))
        if len(states) == 1:
            return states[0]
        else:
            return self.env['res.country.state'].create({
                'name': row[name_row_index],
                'code': row[code_row_index],
                'country_id': country_id
                })

    @api.one
    def run_import(self):
        bzip_obj = self.env['res.better.zip']
        country_id = self.country_id.id
        country_code = self.country_id.code.upper()
        config_url = self.pool['ir.config_parameter'].get_param(
            self._cr, self._uid, 'geonames.url',
            default='http://download.geonames.org/export/zip/%s.zip')
        url = config_url % country_code
        logger.info('Starting to download %s' % url)
        res_request = requests.get(url)
        if res_request.status_code != requests.codes.ok:
            raise Warning(
                _('Error:'),
                _('Got an error %d when trying to download the file %s.')
                % (res_request.status_code, url))
        bzip_ids_to_delete = bzip_obj.search([('country_id', '=', country_id)])
        if bzip_ids_to_delete:
            bzip_ids_to_delete.unlink()
            logger.info(
                '%d better zip entries deleted for country %s'
                % (len(bzip_ids_to_delete), self.country_id.name))
        f_geonames = zipfile.ZipFile(StringIO.StringIO(res_request.content))
        tempdir = tempfile.mkdtemp(prefix='openerp')
        f_geonames.extract('%s.txt' % country_code, tempdir)
        logger.info('The geonames zipfile has been decompressed')
        data_file = open(os.path.join(tempdir, '%s.txt' % country_code), 'r')
        data_file.seek(0)
        logger.info(
            'Starting to create the better zip entries')
        for row in unicodecsv.reader(
                data_file, encoding='utf-8', delimiter='	'):
            self.create_better_zip(row, country_id, country_code)
        data_file.close()
        logger.info(
            'The wizard to create better zip entries from geonames '
            'has been successfully completed.')
        return True
