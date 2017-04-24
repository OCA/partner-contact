# -*- coding: utf-8 -*-
# © 2014-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# © 2014 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# © 2016 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError
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
    letter_case = fields.Selection([
        ('unchanged', 'Unchanged'),
        ('title', 'Title Case'),
        ('upper', 'Upper Case'),
        ], string='Letter Case', default='unchanged',
        help="Converts retreived city and state names to Title Case "
        "(upper case on each first letter of a word) or Upper Case "
        "(all letters upper case).")

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
            'latitude': row[9],
            'longitude': row[10],
            }
        return vals

    @api.model
    def create_better_zip(self, row, country):
        if row[0] != country.code:
            raise UserError(
                _("The country code inside the file (%s) doesn't "
                    "correspond to the selected country (%s).")
                % (row[0], country.code))
        logger.debug('ZIP = %s - City = %s' % (row[1], row[2]))
        if self.letter_case == 'title':
            row[2] = row[2].title()
            row[3] = row[3].title()
        elif self.letter_case == 'upper':
            row[2] = row[2].upper()
            row[3] = row[3].upper()
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
        else:  # pragma: no cover
            return False

    @tools.ormcache('country_id', 'code')
    def _get_state(self, country_id, code, name):
        state = self.env['res.country.state'].search(
            [('country_id', '=', country_id),
             ('code', '=', code)], limit=1,
        )
        if state:  # pragma: no cover
            return state
        else:
            return self.env['res.country.state'].create({
                'name': name,
                'code': code,
                'country_id': country_id,
            })

    @api.model
    def select_or_create_state(
            self, row, country, code_row_index=4, name_row_index=3):
        return self._get_state(
            country.id, row[code_row_index], row[name_row_index],
        )

    @api.multi
    def run_import(self):
        self.ensure_one()
        zip_model = self.env['res.better.zip']
        country_code = self.country_id.code
        config_url = self.env['ir.config_parameter'].get_param(
            'geonames.url',
            default='http://download.geonames.org/export/zip/%s.zip')
        url = config_url % country_code
        logger.info('Starting to download %s' % url)
        res_request = requests.get(url)
        if res_request.status_code != requests.codes.ok:
            raise UserError(
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
        max_import = self.env.context.get('max_import', 0)
        reader = unicodecsv.reader(data_file, encoding='utf-8', delimiter='	')
        for i, row in enumerate(reader):
            zip_code = self.create_better_zip(row, self.country_id)
            if zip_code in zips_to_delete:
                zips_to_delete -= zip_code
            if max_import and (i + 1) == max_import:
                break
        data_file.close()
        if zips_to_delete and not max_import:
            zips_to_delete.unlink()
            logger.info('%d better zip entries deleted for country %s' %
                        (len(zips_to_delete), self.country_id.name))
        logger.info(
            'The wizard to create better zip entries from geonames '
            'has been successfully completed.')
        return True
