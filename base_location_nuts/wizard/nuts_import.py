# Copyright 2015 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2017 David Vidal <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import UserError
import requests
import re
import logging
from lxml import etree
from collections import OrderedDict

logger = logging.getLogger(__name__)

# Default server values
URL_BASE = 'https://ec.europa.eu'
URL_PATH = '/eurostat/ramon/nomenclatures/index.cfm'
URL_PARAMS = {'TargetUrl': 'ACT_OTH_CLS_DLD',
              'StrNom': 'NUTS_2013',
              'StrFormat': 'XML',
              'StrLanguageCode': 'EN',
              'StrLayoutCode': 'HIERARCHIC'
              }


class NutsImport(models.TransientModel):
    _name = 'nuts.import'
    _description = 'Import NUTS items from European RAMON service'
    _parents = [False, False, False, False]
    _countries = {
        "BE": False,
        "BG": False,
        "CZ": False,
        "DK": False,
        "DE": False,
        "EE": False,
        "IE": False,
        "GR": False,  # EL
        "ES": False,
        "FR": False,
        "HR": False,
        "IT": False,
        "CY": False,
        "LV": False,
        "LT": False,
        "LU": False,
        "HU": False,
        "MT": False,
        "NL": False,
        "AT": False,
        "PL": False,
        "PT": False,
        "RO": False,
        "SI": False,
        "SK": False,
        "FI": False,
        "SE": False,
        "GB": False,  # UK
    }
    _current_country = False
    _map = OrderedDict([
        ('level', {
            'xpath': '', 'attrib': 'idLevel',
            'type': 'integer', 'required': True}),
        ('code', {
            'xpath': './Label/LabelText[@language="ALL"]',
            'type': 'string', 'required': True}),
        ('name', {
            'xpath': './Label/LabelText[@language="EN"]',
            'type': 'string', 'required': True}),
    ])

    def _check_node(self, node):
        if node.get('id') and node.get('idLevel'):
            return True
        return False

    def _mapping(self, node):
        item = {}
        for k, v in self._map.items():
            field_xpath = v.get('xpath', '')
            field_attrib = v.get('attrib', False)
            field_type = v.get('type', 'string')
            field_required = v.get('required', False)
            value = ''
            if field_xpath:
                n = node.find(field_xpath)
            else:
                n = node
            if n is not None:
                if field_attrib:
                    value = n.get(field_attrib, '')
                else:
                    value = n.text
                if field_type == 'integer':
                    try:
                        value = int(value)
                    except (ValueError, TypeError):
                        logger.warn(
                            "Value %s for field %s replaced by 0" %
                            (value, k))
                        value = 0
            else:
                logger.debug("xpath = '%s', not found" % field_xpath)
            if field_required and not value:
                raise UserError(
                    _('Value not found for mandatory field %s' % k))
            item[k] = value
        return item

    def _download_nuts(self, url_base=None, url_path=None, url_params=None):
        if not url_base:
            url_base = URL_BASE
        if not url_path:
            url_path = URL_PATH
        if not url_params:
            url_params = URL_PARAMS
        url = url_base + url_path + '?'
        url += '&'.join([k + '=' + v for k, v in url_params.items()])
        logger.info('Starting to download %s' % url)
        try:
            res_request = requests.get(url)
        except Exception as e:
            raise UserError(
                _('Got an error when trying to download the file: %s.') %
                str(e))
        if res_request.status_code != requests.codes.ok:
            raise UserError(
                _('Got an error %d when trying to download the file %s.')
                % (res_request.status_code, url))
        logger.info('Download successfully %d bytes' %
                    len(res_request.content))
        # Workaround XML: Remove all characters before <?xml
        pattern = re.compile(rb'^.*<\?xml', re.DOTALL)
        content_fixed = re.sub(pattern, b'<?xml', res_request.content)
        if not re.match(rb'<\?xml', content_fixed):
            raise UserError(_('Downloaded file is not a valid XML file'))
        return content_fixed

    @api.model
    def _load_countries(self):
        for k in self._countries:
            self._countries[k] = self.env['res.country'].search(
                [('code', '=', k)])
        # Workaround to translate some country codes:
        #   EL => GR (Greece)
        #   UK => GB (United Kingdom)
        self._countries['EL'] = self._countries['GR']
        self._countries['UK'] = self._countries['GB']

    @api.model
    def state_mapping(self, data, node):
        # Method to inherit and add state_id relation depending on country
        level = data.get('level', 0)
        code = data.get('code', '')
        if level == 1:
            self._current_country = self._countries[code]
        return {
            'country_id': self._current_country.id,
        }

    @api.model
    def create_or_update_nuts(self, node):
        if not self._check_node(node):
            return False

        nuts_model = self.env['res.partner.nuts']
        data = self._mapping(node)
        data.update(self.state_mapping(data, node))
        level = data.get('level', 0)
        if level >= 2 and level <= 5:
            data['parent_id'] = self._parents[level - 2]
        nuts = nuts_model.search([('level', '=', data['level']),
                                  ('code', '=', data['code'])])
        if nuts:
            nuts.filtered(lambda n: not n.not_updatable).write(data)
        else:
            if data.get('country_id', False):
                nuts = nuts_model.create(data)
            else:
                logger.info(_('Missing country_id for %s') % data)
        if level >= 1 and level <= 4:
            self._parents[level - 1] = nuts.id
        return nuts

    @api.multi
    def run_import(self):
        nuts_model = self.env['res.partner.nuts'].\
            with_context(defer_parent_store_computation=True)
        self._load_countries()
        # All current NUTS (for available countries),
        #   delete if not found above
        nuts_to_delete = nuts_model.search(
            [('country_id', 'in', [x.id for x in self._countries.values()]),
             ('not_updatable', '=', False)])
        # Download NUTS in english, create or update
        logger.info('Importing NUTS 2013 English...')
        xmlcontent = self._download_nuts()
        dom = etree.fromstring(xmlcontent)
        for node in dom.iter('Item'):
            logger.debug('Reading level=%s, id=%s',
                         node.get('idLevel', 'N/A'),
                         node.get('id', 'N/A'))
            nuts = self.create_or_update_nuts(node)
            if nuts and nuts in nuts_to_delete:
                nuts_to_delete -= nuts
        # Delete obsolete NUTS
        if nuts_to_delete:
            logger.info('%d NUTS entries deleted' % len(nuts_to_delete))
            nuts_to_delete.unlink()
        logger.info(
            'The wizard to create NUTS entries from RAMON '
            'has been successfully completed.')
        return True
