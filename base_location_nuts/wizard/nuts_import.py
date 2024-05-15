# Copyright 2015 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2017 David Vidal <jairo.llopis@tecnativa.com>
# Copyright 2021 Andrii Skrypka <andrijskrypa@ukr.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

import requests

from odoo import _, api, models

logger = logging.getLogger(__name__)

ENDPOINT = "https://publications.europa.eu/webapi/rdf/sparql"


class NutsImport(models.TransientModel):
    """
    Wizard to import the NUTS data from the new ShowVoc endpoint
    https://showvoc.op.europa.eu/ as RAMON is deprecated. The data is stored in
    a SPARQL database in a Resource Description Framework (RDF) format.

    Each element is a resource given in the format of an XML file. The data is
    related semantically by the SKOS thesaurus (https://www.w3.org/TR/skos-reference/)
    and the NACE2 thesaurus (https://data.europa.eu/ux2/nace2/). Also a element
    is identified by a unique URI code, and used as a foreing key in the related
    elements.

    The wizard creates the partner nuts and adds the parent child relation. then
    it deletes the obsolete nuts entries unless they are marked as not updatable.
    """

    _name = "nuts.import"
    _description = "Import NUTS items from European ShowVoc service"
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
    }

    @api.model
    def _load_countries(self):
        for k in self._countries:
            self._countries[k] = self.env["res.country"].search([("code", "=", k)])
        # Workaround to translate some country codes:
        #   EL => GR (Greece)
        self._countries["EL"] = self._countries["GR"]

    # flake8: noqa: B950
    def _get_query(self):
        query = """
            PREFIX : <http://data.europa.eu/nuts/>
            PREFIX adms: <http://www.w3.org/ns/adms#>
            PREFIX corrStatus: <http://publications.europa.eu/resource/authority/correction-status/>
            PREFIX cpsv: <http://purl.org/vocab/cpsv#>
            PREFIX cv: <http://data.europa.eu/m8g/>
            PREFIX dataTypeDefinitions: <http://publications.europa.eu/ontology/euvoc/dataTypeDefinitions#>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            PREFIX dcat: <http://www.w3.org/ns/dcat#>
            PREFIX dct: <http://purl.org/dc/terms/>
            PREFIX eli: <http://data.europa.eu/eli/ontology#>
            PREFIX euvoc: <http://publications.europa.eu/ontology/euvoc#>
            PREFIX externalImports: <http://publications.europa.eu/ontology/euvoc/externalImports#>
            PREFIX fn: <http://www.w3.org/2005/xpath-functions#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX geosparql: <http://www.opengis.net/ont/geosparql#>
            PREFIX gml: <http://www.opengis.net/ont/gml#>
            PREFIX gn: <http://www.geonames.org/ontology#>
            PREFIX grddl: <http://www.w3.org/2003/g/data-view#>
            PREFIX internalImports: <http://publications.europa.eu/ontology/euvoc/internalImports#>
            PREFIX legalDescriptions: <http://publications.europa.eu/ontology/euvoc/legalDescriptions#>
            PREFIX lemon: <http://lemon-model.net/lemon#>
            PREFIX lexinfo: <http://www.lexinfo.net/ontology/2.0/lexinfo#>
            PREFIX lexvo: <http://lexvo.org/ontology#>
            PREFIX linguisticDescriptions: <http://publications.europa.eu/ontology/euvoc/linguisticDescriptions#>
            PREFIX locn: <https://www.w3.org/ns/locn#>
            PREFIX luc: <http://www.ontotext.com/owlim/lucene#>
            PREFIX oa: <http://www.w3.org/ns/oa#>
            PREFIX ontology: <https://www.geonames.org/ontology#>
            PREFIX org: <http://www.w3.org/ns/org#>
            PREFIX organisationDescriptions: <http://publications.europa.eu/ontology/euvoc/organisationDescriptions#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX qb: <http://purl.org/linked-data/cube#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdf4j: <http://rdf4j.org/schema/rdf4j#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX schema: <http://schema.org/>
            PREFIX sesame: <http://www.openrdf.org/schema/sesame#>
            PREFIX sf: <http://www.opengis.net/ont/sf#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>
            PREFIX spatial: <http://geovocab.org/mappings/spatial#>
            PREFIX spatialDescriptions: <http://publications.europa.eu/ontology/euvoc/spatialDescriptions#>
            PREFIX spdx: <http://spdx.org/rdf/terms#>
            PREFIX tableDescriptions: <http://publications.europa.eu/ontology/euvoc/tableDescriptions#>
            PREFIX temporalDescriptions: <http://publications.europa.eu/ontology/euvoc/temporalDescriptions#>
            PREFIX terms: <'http://purl.org/dc/terms/>
            PREFIX time: <http://www.w3.org/2006/time#>
            PREFIX vann: <http://purl.org/vocab/vann/>
            PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
            PREFIX wgs: <http://www.w3.org/2003/01/geo/wgs84_pos#>
            PREFIX xkos: <http://rdf-vocabulary.ddialliance.org/xkos#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

            SELECT ?s ?code ?region_name ?level ?parent WHERE {
                ?s a skos:Concept;
                skos:inScheme ?scheme;
                        skosxl:prefLabel ?Region;
                        skos:altLabel ?name;
                        :level ?level;
                    skos:notation ?code .
                OPTIONAL {?s :regionOrder ?regionOrder .}
                OPTIONAL {?s skos:broader ?BT . ?BT skos:notation ?BT_Code. }
                BIND (STR(?BT_Code) as ?parent )
                ?Region skosxl:literalForm ?region_name .
                ?scheme skosxl:prefLabel ?Label.
                ?Label skosxl:literalForm ?Name .

                FILTER ( ?scheme = <http://data.europa.eu/nuts/scheme/2024> )
            }
            ORDER BY ?s
        """
        return query

    def _delete_obsolete_nuts(self, new_nuts_ids):
        """Deletes the NUTS entries that are not updatable."""
        nuts_to_delete = new_nuts_ids.search([("not_updatable", "=", False)])
        nuts_to_delete = nuts_to_delete - new_nuts_ids
        if not nuts_to_delete:
            logger.info("No NUTS entries to delete.")
            return
        max_level = max(nuts_to_delete.mapped("level"))
        for level in range(max_level, 0, -1):
            ntd2 = nuts_to_delete.filtered(lambda nut: nut.level == level)
            ntd2.unlink()
            nuts_to_delete -= ntd2
        logger.info("%d NUTS entries deleted" % len(nuts_to_delete))

    def _create_partner_nuts(self, nuts_data):
        """Creates or updates NUTS regions from the given GET request."""
        nuts_ids = self.env["res.partner.nuts"]
        nuts_json = nuts_data.json()
        bindings = nuts_json.get("results", {}).get("bindings", [])
        all_nuts = nuts_ids.search_read([], ["code"])
        nuts_map = {nut.get("code"): nut.get("id") for nut in all_nuts}
        for binding in bindings:
            code = binding.get("code", {}).get("value")
            region_name = binding.get("region_name", {}).get("value")
            name = region_name.replace(f"{code} ", "")
            level_char = binding.get("level", {}).get("value")
            level = (
                int(level_char) + 1 if level_char and level_char.isdigit() else False
            )
            parent = binding.get("parent", {}).get("value")
            parent_id = nuts_map.get(parent, False)
            country_id = False
            if code and self._countries.get(code[:2], False):
                country_id = self._countries[code[:2]].id
            binding_data = {
                "name": name,
                "code": code,
                "parent_id": parent_id,
                "level": level,
                "country_id": country_id,
            }
            if code in nuts_map:
                nut = nuts_ids.browse(nuts_map[code])
                if not nut.not_updatable:
                    nut.write(binding_data)
            else:
                nut = nuts_ids.create(binding_data)
                nuts_map.update({nut.code: nut.id})
            nuts_ids |= nut
        self._delete_obsolete_nuts(nuts_ids)
        logger.info(
            "The wizard to create NUTS entries from ShowVoc has been"
            "successfully completed."
        )
        return nuts_ids

    def import_update_partner_nuts(self):
        self._load_countries()
        query = self._get_query()
        response = requests.get(
            ENDPOINT, params={"format": "json", "query": query}, timeout=120
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            logger.error(
                "Error %s while trying to connect to the ShowVoc service: %s",
                error.response.status_code,
                error.response.text,
            )
            raise error
        nuts_ids = self._create_partner_nuts(response)
        return nuts_ids

    def action_partner_nuts(self):
        nuts_ids = self.import_update_partner_nuts()
        tree_view_id = self.env.ref("base_location_nuts.res_partner_nuts_tree").id
        return {
            "name": _("Partner NUTS by EU"),
            "view_mode": "tree",
            "res_model": "res.partner.nuts",
            "view_id": tree_view_id,
            "type": "ir.actions.act_window",
            "domain": [("id", "=", nuts_ids.ids)],
        }
