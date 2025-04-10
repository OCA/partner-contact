# Copyright 2014-2016 Akretion (Alexis de Lattre
#                     <alexis.delattre@akretion.com>)
# Copyright 2014 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# Copyright 2017 ForgeFlow, S.L. <.com>
# Copyright 2018 Aitor Bouzas <aitor.bouzas@adaptivecity.com>
# Copyright 2016-2022 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import csv
import io
import logging
import os
import tempfile
import zipfile

import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)


class CityZipGeonamesImport(models.TransientModel):
    _name = "city.zip.geonames.import"
    _description = "Import City Zips from Geonames"

    country_ids = fields.Many2many("res.country", string="Countries")

    letter_case = fields.Selection(
        [("unchanged", "Unchanged"), ("title", "Title Case"), ("upper", "Upper Case")],
        default="unchanged",
        help="Converts retreived city and state names to Title Case "
        "(upper case on each first letter of a word) or Upper Case "
        "(all letters upper case).",
    )

    @api.model
    def transform_city_name(self, city, country):
        """Override it for transforming city name (if needed)
        :param city: Original city name
        :param country: Country record
        :return: Transformed city name
        """
        res = city
        if self.letter_case == "title":
            res = city.title()
        elif self.letter_case == "upper":
            res = city.upper()
        return res

    @api.model
    def _domain_search_city_zip(self, row, city=False):
        domain = [("name", "=", row[1])]
        if city:
            domain += [("city_id", "=", city.id)]
        return domain

    @api.model
    def _select_city(self, row, country, state):
        return self.env["res.city"].search(
            [
                ("name", "=", self.transform_city_name(row[2], country)),
                ("country_id", "=", country.id),
                ("state_id", "=", state.id),
            ],
            limit=1,
        )

    @api.model
    def _select_zip(self, row, country, state):
        city = self._select_city(row, country, state)
        return self.env["res.city.zip"].search(self._domain_search_city_zip(row, city))

    @api.model
    def prepare_state(self, row, country):
        return {
            "name": row[country.geonames_state_name_column or 3],
            "code": row[country.geonames_state_code_column or 4],
            "country_id": country.id,
        }

    @api.model
    def prepare_city(self, row, country, state):
        vals = {
            "name": self.transform_city_name(row[2], country),
            "state_id": state.id,
            "country_id": country.id,
        }
        return vals

    @api.model
    def prepare_zip(self, row, city_id):
        vals = {"name": row[1], "city_id": city_id}
        return vals

    @api.model
    def get_and_parse_csv(self, country):
        country_code = country.code
        config_url = self.env["ir.config_parameter"].get_param(
            "geonames.url", default="http://download.geonames.org/export/zip/%s.zip"
        )
        url = config_url % country_code
        logger.info("Starting to download %s" % url)
        res_request = requests.get(url, timeout=15)
        if res_request.status_code != requests.codes.ok:
            # pylint: disable=translation-positional-used - Don't want to re-translate
            raise UserError(
                _("Got an error %d when trying to download the file %s.")
                % (res_request.status_code, url)
            )

        f_geonames = zipfile.ZipFile(io.BytesIO(res_request.content))
        tempdir = tempfile.mkdtemp(prefix="odoo")
        f_geonames.extract("%s.txt" % country_code, tempdir)

        data_file = open(
            os.path.join(tempdir, "%s.txt" % country_code), encoding="utf-8"
        )
        data_file.seek(0)
        reader = csv.reader(data_file, delimiter="	")
        parsed_csv = [row for i, row in enumerate(reader)]
        data_file.close()
        logger.info("The geonames zipfile has been decompressed")
        return parsed_csv

    def _create_states(self, parsed_csv, search_states, max_import, country):
        states_map = {}
        if search_states:
            states_map = {
                state.code: state
                for state in self.env["res.country.state"].search(
                    [("country_id", "=", country.id)]
                )
            }
        # States
        state_vals_set = set()
        state_dict = {}
        for i, row in enumerate(parsed_csv):
            if max_import and i == max_import:
                break
            state = None
            if search_states:
                code = row[country.geonames_state_code_column or 4]
                state = states_map.get(code)
            if not state:
                state_vals = self.prepare_state(row, country)
                state_vals_set.add(
                    (state_vals["name"], state_vals["code"], state_vals["country_id"])
                )
            else:
                state_dict[state.code] = state
        state_vals_list = [
            {"name": name, "code": code, "country_id": country_id}
            for name, code, country_id in state_vals_set
        ]
        logger.info("Importing %d states", len(state_vals_list))
        created_states = self.env["res.country.state"].create(state_vals_list)
        for i, vals in enumerate(state_vals_list):
            state_dict[vals["code"]] = created_states[i]
        return state_dict

    def _create_cities(
        self, parsed_csv, search_cities, max_import, state_dict, country
    ):
        # Cities
        city_vals_set = set()
        city_dict = {}
        for i, row in enumerate(parsed_csv):
            if max_import and i == max_import:
                break
            state = state_dict[row[country.geonames_state_code_column or 4]]
            city = (
                self._select_city(row, country, state)
                if search_cities
                else self.env["res.city"]
            )
            if not city:
                city_vals = self.prepare_city(row, country, state)
                city_vals_set.add(
                    (city_vals["name"], city_vals["state_id"], city_vals["country_id"])
                )
            else:
                city_dict[(city.name, state.id)] = city.id
        city_vals_list = [
            {"name": name, "state_id": state_id, "country_id": country_id}
            for name, state_id, country_id in city_vals_set
        ]
        logger.info("Importing %d cities", len(city_vals_list))
        created_cities = self.env["res.city"].create(city_vals_list)
        for i, vals in enumerate(city_vals_list):
            city_dict[(vals["name"], vals["state_id"])] = created_cities[i].id
        return city_dict

    def run_import(self):
        for country in self.country_ids:
            parsed_csv = self.get_and_parse_csv(country)
            self._process_csv(parsed_csv, country)
        return True

    def _action_remove_old_records(self, model_name, old_records, country):
        model = self.env[model_name]
        items = model.browse(list(old_records))
        try:
            logger.info("removing %s entries" % model._name)
            items.unlink()
            logger.info(
                "%d entries deleted for country %s" % (len(old_records), country.name)
            )
        except Exception:
            for item in items:
                try:
                    item.unlink()
                except Exception:
                    logger.info(_("%d could not be deleted %") % item.name)

    def _process_csv(self, parsed_csv, country):
        state_model = self.env["res.country.state"]
        zip_model = self.env["res.city.zip"]
        res_city_model = self.env["res.city"]
        # Store current record list
        old_zips = set(zip_model.search([("city_id.country_id", "=", country.id)]).ids)
        search_zips = len(old_zips) > 0
        old_cities = set(res_city_model.search([("country_id", "=", country.id)]).ids)
        search_cities = len(old_cities) > 0
        current_states = state_model.search([("country_id", "=", country.id)])
        search_states = len(current_states) > 0
        max_import = self.env.context.get("max_import", 0)
        logger.info("Starting to create the cities and/or city zip entries")
        # Pre-create states and cities
        state_dict = self._create_states(parsed_csv, search_states, max_import, country)
        city_dict = self._create_cities(
            parsed_csv, search_cities, max_import, state_dict, country
        )
        # Zips
        zip_vals_list = []
        for i, row in enumerate(parsed_csv):
            if max_import and i == max_import:
                break
            # Don't search if there aren't any records
            zip_code = False
            state = state_dict[row[country.geonames_state_code_column or 4]]
            if search_zips:
                zip_code = self._select_zip(row, country, state)
            if not zip_code:
                city_id = city_dict[
                    (self.transform_city_name(row[2], country), state.id)
                ]
                zip_vals = self.prepare_zip(row, city_id)
                if zip_vals not in zip_vals_list:
                    zip_vals_list.append(zip_vals)
            else:
                old_zips -= set(zip_code.ids)
        zip_model.create(zip_vals_list)
        if not max_import:
            if old_zips:
                self._action_remove_old_records("res.city.zip", old_zips, country)
            old_cities -= set(city_dict.values())
            if old_cities:
                self._action_remove_old_records("res.city", old_cities, country)
        logger.info(
            "The wizard to create cities and/or city zip entries from "
            "geonames has been successfully completed."
        )
        return True
