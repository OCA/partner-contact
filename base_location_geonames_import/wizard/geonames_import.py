# -*- encoding: utf-8 -*-
##############################################################################
#
#    Base Location Geonames Import module for OpenERP
#    Copyright (C) 2014 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
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

from openerp.osv import orm, fields
from openerp.tools.translate import _
import requests
import tempfile
import StringIO
import unicodecsv
import zipfile
import os
import logging

logger = logging.getLogger(__name__)


class better_zip_geonames_import(orm.TransientModel):
    _name = 'better.zip.geonames.import'
    _description = 'Import Better Zip from Geonames'

    _columns = {
        'country_id': fields.many2one('res.country', 'Country', required=True),
    }

    def _prepare_better_zip(
            self, cr, uid, row, country_id, states, context=None):
        '''This function is designed to be inherited'''
        state_id = False
        if states and row[4] and row[4] in states:
            state_id = states[row[4].upper()]
        vals = {
            'name': row[1],
            'city': row[2],
            'state_id': state_id,
            'country_id': country_id,
            }
        return vals

    def create_better_zip(
            self, cr, uid, row, country_id, country_code, states,
            context=None):
        bzip_id = False
        if row[0] != country_code:
            raise orm.except_orm(
                _('Error:'),
                _("The country code inside the file (%s) doesn't "
                    "correspond to the selected country (%s).")
                % (row[0], country_code))
        logger.debug('ZIP = %s - City = %s' % (row[1], row[2]))
        if row[1] and row[2]:
            vals = self._prepare_better_zip(
                cr, uid, row, country_id, states, context=context)
            if vals:
                bzip_id = self.pool['res.better.zip'].create(
                    cr, uid, vals, context=context)
        return bzip_id

    def run_import(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'Only one ID for the better zip import wizard'
        bzip_obj = self.pool['res.better.zip']
        wizard = self.browse(cr, uid, ids[0], context=context)
        country_id = wizard.country_id.id
        country_code = wizard.country_id.code.upper()
        url = 'http://download.geonames.org/export/zip/%s.zip' % country_code
        logger.info('Starting to download %s' % url)
        res_request = requests.get(url)
        if res_request.status_code != requests.codes.ok:
            raise orm.except_orm(
                _('Error:'),
                _('Got an error %d when trying to download the file %s.')
                % (res_request.status_code, url))
        bzip_ids_to_delete = bzip_obj.search(
            cr, uid, [('country_id', '=', country_id)], context=context)
        if bzip_ids_to_delete:
            cr.execute('SELECT id FROM res_better_zip WHERE id in %s '
                'FOR UPDATE NOWAIT', (tuple(bzip_ids_to_delete), ))
            bzip_obj.unlink(cr, uid, bzip_ids_to_delete, context=context)
            logger.info(
                '%d better zip entries deleted for country %s'
                % (len(bzip_ids_to_delete), wizard.country_id.name))
        state_ids = self.pool['res.country.state'].search(
            cr, uid, [('country_id', '=', country_id)], context=context)
        states = {}
        # key = code of the state ; value = ID of the state in OpenERP
        if state_ids:
            states_r = self.pool['res.country.state'].read(
                cr, uid, state_ids, ['code', 'country_id'], context=context)
            for state in states_r:
                states[state['code'].upper()] = state['id']
        f_geonames = zipfile.ZipFile(StringIO.StringIO(res_request.content))
        tempdir = tempfile.mkdtemp(prefix='openerp')
        f_geonames.extract('%s.txt' % country_code, tempdir)
        logger.info('The geonames zipfile has been decompressed')
        data_file = open(os.path.join(tempdir, '%s.txt' % country_code), 'r')
        data_file.seek(0)
        logger.info(
            'Starting to create the better zip entries %s state information'
            % (states and 'with' or 'without'))
        for row in unicodecsv.reader(
                data_file, encoding='utf-8', delimiter='	'):
            self.create_better_zip(
                cr, uid, row, country_id, country_code, states,
                context=context)
        data_file.close()
        logger.info(
            'The wizard to create better zip entries from geonames '
            'has been successfully completed.')
        return True
