# Copyright 2014-2016 Akretion (Alexis de Lattre
#                     <alexis.delattre@akretion.com>)
# Copyright 2014 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
#                <contact@eficent.com>
# Copyright 2018 Aitor Bouzas <aitor.bouzas@adaptivecity.com>
# Copyright 2016-2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
import requests
import tempfile
import io
import zipfile
import os
import logging
import csv

logger = logging.getLogger(__name__)


class CityZipGeonamesImport(models.TransientModel):
    _name = 'city.zip.geonames.import'
    _description = 'Import City Zips from Geonames'
    _rec_name = 'country_id'

    country_id = fields.Many2one('res.country', 'Country', required=True)
    code_row_index = fields.Integer(
        related='country_id.geonames_state_code_column',
        readonly=True)
    name_row_index = fields.Integer(
        related='country_id.geonames_state_name_column')

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
        res = city
        if self.letter_case == 'title':
            res = city.title()
        elif self.letter_case == 'upper':
            res = city.upper()
        return res

    @api.model
    def _domain_search_res_city(self, row, country):
        return [('name', '=', self.transform_city_name(row[2], country)),
                ('country_id', '=', country.id)]

    @api.model
    def _domain_search_city_zip(self, row, res_city):
        domain = [('name', '=', row[1])]
        if res_city:
            domain += [('city_id', '=', res_city.id)]
        return domain

    @api.model
    def select_state(self, row, country):
        code = row[self.code_row_index or 4]
        return self.env['res.country.state'].search(
            [('country_id', '=', country.id),
             ('code', '=', code)], limit=1,
        )

    @api.model
    def select_city(self, row, country):
        res_city_model = self.env['res.city']
        return res_city_model.search(self._domain_search_res_city(
            row, country), limit=1)

    @api.model
    def select_zip(self, row, country):
        city = self.select_city(row, country)
        return self.env['res.city.zip'].search(self._domain_search_city_zip(
            row, city))

    @api.model
    def prepare_state(self, row, country):
        return {
            'name': row[self.name_row_index or 3],
            'code': row[self.code_row_index or 4],
            'country_id': country.id,
        }

    @api.model
    def prepare_city(self, row, country, state_id):
        vals = {
            'name': self.transform_city_name(row[2], country),
            'state_id': state_id,
            'country_id': country.id,
        }
        return vals

    @api.model
    def prepare_zip(self, row, city_id):
        vals = {
            'name': row[1],
            'city_id': city_id,
        }
        return vals

    @api.model
    def get_and_parse_csv(self):
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

        f_geonames = zipfile.ZipFile(io.BytesIO(res_request.content))
        tempdir = tempfile.mkdtemp(prefix='odoo')
        f_geonames.extract('%s.txt' % country_code, tempdir)

        data_file = open(os.path.join(tempdir, '%s.txt' % country_code), 'r',
                         encoding='utf-8')
        data_file.seek(0)
        reader = csv.reader(data_file, delimiter='	')
        parsed_csv = [row for i, row in enumerate(reader)]
        data_file.close()
        logger.info('The geonames zipfile has been decompressed')
        return parsed_csv

    def _create_states(self, parsed_csv, search_states, max_import):
        # States
        state_vals_list = []
        state_dict = {}
        for i, row in enumerate(parsed_csv):
            if max_import and i == max_import:
                break
            state = self.select_state(
                row, self.country_id) if search_states else False
            if not state:
                state_vals = self.prepare_state(row, self.country_id)
                if state_vals not in state_vals_list:
                    state_vals_list.append(state_vals)
            else:
                state_dict[state.code] = state.id

        created_states = self.env['res.country.state'].create(state_vals_list)
        for i, vals in enumerate(state_vals_list):
            state_dict[vals['code']] = created_states[i].id
        return state_dict

    def _create_cities(self, parsed_csv,
                       search_cities, max_import, state_dict):
        # Cities
        city_vals_list = []
        city_dict = {}
        for i, row in enumerate(parsed_csv):
            if max_import and i == max_import:
                break
            state_id = state_dict[row[self.code_row_index or 4]]
            city = self.select_city(
                row, self.country_id) if search_cities else False
            if not city:
                city_vals = self.prepare_city(
                    row, self.country_id, state_id)
                if city_vals not in city_vals_list:
                    city_vals_list.append(city_vals)
            else:
                city_dict[(city.name, state_id)] = city.id
        created_cities = self.env['res.city'].create(city_vals_list)
        for i, vals in enumerate(city_vals_list):
            city_dict[(vals['name'], vals['state_id'])] = created_cities[i].id
        return city_dict

    def run_import(self):
        self.ensure_one()
        parsed_csv = self.get_and_parse_csv()
        return self._process_csv(parsed_csv)

    def _process_csv(self, parsed_csv):
        state_model = self.env['res.country.state']
        zip_model = self.env['res.city.zip']
        res_city_model = self.env['res.city']

        # Store current record list
        current_zips = zip_model.search(
            [('city_id.country_id', '=', self.country_id.id)])
        search_zips = True and len(current_zips) > 0 or False
        current_cities = res_city_model.search(
            [('country_id', '=', self.country_id.id)])
        search_cities = True and len(current_cities) > 0 or False
        current_states = state_model.search(
            [('country_id', '=', self.country_id.id)])
        search_states = True and len(current_states) > 0 or False

        max_import = self.env.context.get('max_import', 0)
        logger.info('Starting to create the cities and/or city zip entries')

        state_dict = self._create_states(parsed_csv,
                                         search_states, max_import)
        city_dict = self._create_cities(parsed_csv,
                                        search_cities, max_import, state_dict)

        # Zips
        zip_vals_list = []
        for i, row in enumerate(parsed_csv):
            if max_import and i == max_import:
                break
            # Don't search if there aren't any records
            zip_code = False
            if search_zips:
                zip_code = self.select_zip(row, self.country_id)
            if not zip_code:
                state_id = state_dict[row[self.code_row_index or 4]]
                city_id = city_dict[(
                    self.transform_city_name(row[2], self.country_id),
                    state_id,
                )]
                zip_vals = self.prepare_zip(row, city_id)
                if zip_vals not in zip_vals_list:
                    zip_vals_list.append(zip_vals)

        delete_zips = self.env['res.city.zip'].create(zip_vals_list)
        current_zips -= delete_zips

        if not max_import:
            current_zips.unlink()
            logger.info('%d city zip entries deleted for country %s' %
                        (len(current_zips), self.country_id.name))

            # Since we wrapped the entire cities
            # creation in a function we need
            # to perform a search with city_dict in
            # order to know which are the new ones so
            # we can delete the old ones
            created_cities = res_city_model.search(
                [('country_id', '=', self.country_id.id),
                 ('id', 'in', list(city_dict.values()))]
            )
            current_cities -= created_cities
            current_cities.unlink()
            logger.info('%d res.city entries deleted for country %s' %
                        (len(current_cities), self.country_id.name))
        logger.info(
            'The wizard to create cities and/or city zip entries from '
            'geonames has been successfully completed.')
        return True
