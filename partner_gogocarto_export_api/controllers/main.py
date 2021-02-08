import json
import logging

from odoo import http
from odoo.http import Response, request

_logger = logging.getLogger(__name__)


class PartnerGogocartojs(http.Controller):

    @http.route(
        '/web/<company_id>/get_http_gogocarto_elements',
        methods=['GET'],
        type='http',
        csrf=False,
        auth="public",
        website=True)
    def get_gogocarto_elements_http(self, company_id):
        data = self._jsonify_get_partner(company_id)
        return Response(json.dumps(data))

    def _jsonify_get_partner(self, company_id):
        PartnerSudo = request.env['res.partner'].sudo()
        parser = PartnerSudo._get_gogocarto_parser(company_id)
        partners = PartnerSudo.with_context(force_company=company_id).search(
            PartnerSudo._get_gogocarto_domain(company_id)
            )
        return partners.jsonify(parser)
